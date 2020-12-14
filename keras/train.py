# Originally written by Markus Siemens (MIT; https://github.com/msiemens/HypheNN-de)
# Changes by Egill

import re
from config import *
from predict import predict
import math
from keras.callbacks import ModelCheckpoint
from dataset import int_to_char
from dataset import process_word
from model import model, IncreaseEpochNumber
from time import time
import numpy as np
import keras
import util
import tensorflow as tf
import random
# tf.config.threading.set_intra_op_parallelism_threads(1)
# tf.config.threading.set_inter_op_parallelism_threads(1)


def process_data(words):
    X = []
    y = []
    for i, word in enumerate(words):
        data = process_word(word)
        X.extend(data[0])
        y.extend(data[1])
    return np.asarray(X), np.asarray(y)


words_to_take_as_an_example = []

total_samples_in_dataset = sum(1 for line in open(FILE))

def get_batch():
    while 1:
        f = open(FILE)
        for line in f:
            if(len(line.strip()) >= 2 and not re.search('[^abcdefghijklmnoprstuvwxyzáæéíðóöúýþ.|-]', line.strip())):

                # Not necessary, just here to show examples after each epoch
                if(len(words_to_take_as_an_example) < 200):
                    if(random.random() < 0.2):
                        words_to_take_as_an_example.append(line.strip())

                x_values, y_values = process_word(line.strip())
                yield np.asarray(x_values), np.asarray(y_values)
        f.close()


class predictRandomWord(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        # print()
        print(predict('flugvallarsvæði', self.model))
        print(predict('forsætisráðherrabílstjórarnir', self.model))
        print(predict('líffærafræðilegar', self.model))
        print(predict(
            'vaðlaheiðarvegavinnuverkfærageymsluskúraútidyralyklakippuhringur', self.model))


class Metrics(keras.callbacks.Callback):
    def on_epoch_end(self, batch, logs=None):
        print()
        # global current_epoch
        # current_epoch = current_epoch + 1

        x_validation, y_validation = process_data(words_to_take_as_an_example)

        y_predict = self.model.predict(x_validation)
        total_unhyphened_points = 0
        total_hyphened_points = 0.1
        false_positives = 0
        false_negatives = 0
        incorrect_hyphenation_type = 0
        correct_hyphenation_type = 0
        hyphen_points_found = 0
        false_positives_printed = []

        for index, item in enumerate(y_validation):
            corr = y_validation[index]
            pred = y_predict[index][0]
            if(corr < 0 and pred > 0):
                false_positives += 1
                if(pred > MORPHEME_BREAK_INDICATOR_VALUE):
                    out = ''
                    for row in x_validation[index]:
                        out += int_to_char[np.argmax(row)]
                    out = out[:int(WINDOW_SIZE / 2)] + '\033[91m' + \
                        str(int(round(pred * 10))) + \
                        '\033[0m' + out[int(WINDOW_SIZE / 2):]
                    false_positives_printed.append(out)
            elif(corr > 0 and pred < 0):
                false_negatives += 1
            if(corr > 0):
                total_hyphened_points += 1
                if pred > 0:
                    hyphen_points_found += 1
                    if (abs(pred - corr) < 0.2):
                        correct_hyphenation_type += 1
                    else:
                        incorrect_hyphenation_type += 1
            else:
                total_unhyphened_points += 1
        # exit()

        print('---')
        print('False_positives: ' +
              "{:.0%}".format((false_positives / total_hyphened_points)) +
              ' (' + str(false_positives) + ')'
              )
        if(len(false_positives_printed) > 0):
            print(random.choice(false_positives_printed))
        print('False_negatives: ' +
              "{:.0%}".format((false_negatives / total_hyphened_points)) +
              ' (' + str(false_negatives) + ')')
        # print('Hyphenation points found: ' +
        #       "{:.0%}".format((hyphen_points_found) / total_hyphened_points)+
        #       ' ('+str(hyphen_points_found)+')')
        # print('Hyphenation found but was incorrect type: ' + "{:.2%}".format(incorrect_hyphenation_type / total_hyphened_points))
        print('Correct hyphenation type: ' + "{:.0%}".format(((correct_hyphenation_type) / (total_hyphened_points))) +
              ' (' + str(correct_hyphenation_type) + ')')
        print('---')
        # print('Learning rate: '  )
        # print(OPTIMIZER.lr)
        # print('total_unhyphened_points '+str(total_unhyphened_points))
        # print('total_hyphened_points '+str(total_hyphened_points))
        # print('false_positives '+str(false_positives))
        # print('false_negatives '+str(false_negatives))
        # print('incorrect_hyphenation_type '+str(incorrect_hyphenation_type))
        # print('correct_hyphenation_type '+str(correct_hyphenation_type))
        # print('hyphen_points_found '+str(hyphen_points_found))
        # print('---')
        return


# Limit size of epochs for the large files
epoch_size_multiplier = 1
if(TRAINING_SET == 0 or TRAINING_SET == 4):
    epoch_size_multiplier = epoch_size_multiplier / 20
if(TRAINING_SET == 2):
    epoch_size_multiplier = epoch_size_multiplier * 200

# def get_lr_metric(optimizer):
#     def lr(y_true, y_pred):
#         return optimizer.lr
#     return lr

if __name__ == '__main__':
    start_time = time()
    print('Training model...')
    batch_size = 512 / 2
    model.fit(
        get_batch(),
        batch_size=batch_size,
        steps_per_epoch=math.ceil(
            epoch_size_multiplier * total_samples_in_dataset / batch_size),
        epochs=300,
        callbacks=[
            Metrics(),
            IncreaseEpochNumber(),
            # get_lr_metric(OPTIMIZER),
            predictRandomWord(),
            # keras.callbacks.TensorBoard(write_images=True),
            keras.callbacks.ModelCheckpoint('models/model_latest.h5'),
            # keras.callbacks.ModelCheckpoint('models/model_saved{epoch:08d}.h5', save_freq=5),
            ModelCheckpoint("models/model_best.h5", monitor='loss', verbose=0,
                            save_best_only=True, mode='auto',
                            # save_freq=10
                            ),
            tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5, restore_best_weights = True),
            # tf.keras.callbacks.ReduceLROnPlateau(
            #     monitor="loss",
            #     factor=0.1,
            #     patience=4,
            #     verbose=1,
            #     mode="auto",
            #     min_delta=1E-7,
            #     cooldown=0,
            #     # min_lr=0.0000001,
            # )
        ],


    )

    model.save('models/model_saved.h5')
    print('Done')
    print('Time:', util.time_delta(time() - start_time))

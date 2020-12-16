# Originally written by Markus Siemens (MIT; https://github.com/msiemens/HypheNN-de)
# Changes by Egill

import math

import keras
import tensorflow as tf
import os.path
from os import path
import keras.backend as K
from random import randint
# from train import penalize_false_negatives

from config import *


# if(path.exists('models/model_latest.h5')):
#     print('Loading already-saved model (latest)...')
#     model = keras.models.load_model('models/model_latest.h5')
# elif(path.exists('models/model_best.h5')):
#     print('Loading already-saved model (best)...')
#     model = keras.models.load_model('models/model_best.h5')
# elif(path.exists('models/model_saved.h5')):
#     print('Loading  already-saved model...')
#     model = keras.models.load_model('models/model_saved.h5')
# else:
print('Building model...')

model = keras.models.Sequential()

model.add(keras.layers.Conv1D(
    filters=120,
    kernel_size=3,
    activation='relu',
    input_shape=(WINDOW_SIZE, number_of_possible_letters)
))
model.add(keras.layers.Conv1D(
    filters=600,
    kernel_size=4,  # A total of 7 letters at once
    activation='relu',
))
model.add(keras.layers.Conv1D(
    filters=1000,
    kernel_size=4,  # A total of 11 letters at once
    activation='relu',
))
model.add(keras.layers.Conv1D(
    filters=100,
    kernel_size=1,
    activation='relu',
))
# model.add(keras.layers.Conv1D(
#     filters=50,
#     kernel_size=1,
#     activation='relu',
# ))
model.add(keras.layers.Conv1D(
    filters=10,
    kernel_size=1,
    activation='relu',
))
model.add(keras.layers.Flatten())

# model.add(keras.layers.Dense(80, activation='relu'))
model.add(keras.layers.Dense(40, activation='relu'))
# model.add(keras.layers.Dense(100, activation='relu'))
model.add(keras.layers.Dense(10, activation='relu'))

if __name__ == '__main__':
    model.summary()
    exit()

model.add(keras.layers.Dense(1,activation='linear'))




current_epoch = 1

class IncreaseEpochNumber(keras.callbacks.Callback):
    def on_epoch_end(self, batch, logs=None):
        global current_epoch
        current_epoch = current_epoch + 1
        # print('epoch')

def penalize_false_positives(y_true, y_pred):
    global current_epoch
    fp = false_positives(y_true, y_pred)
    mse = K.mean(K.square(y_pred - y_true))
    # return fp * 100 + mse
    return fp * 30 + mse
    # return fp + mse
    # return fp * (10 + 2 * current_epoch) + mse

def false_positives(y_true, y_pred):
    return K.mean((K.clip((y_pred - y_true - 1.3), 0, 0.8)))
    # return K.mean((K.clip((y_pred - y_true - 0.98), 0, 1)))

# def penalize_false_negatives(y_true, y_pred):
#     global current_epoch
#     fn = false_negatives(y_true, y_pred)
#     mse = K.mean(K.square(y_pred - y_true))
#     # return fp * 100 + mse
#     return fn * (50 + 2 * current_epoch) + mse
# def false_negatives(y_true, y_pred):
#     return K.mean((K.clip((y_true - y_pred - 0.98), 0, 1)))


model.compile(
    optimizer=OPTIMIZER,
    # loss=LOSS,
    loss=penalize_false_positives,
    # loss=penalize_false_negatives, #TEMP!
    metrics=[
        # false_positives,
        # 'accuracy',
        # keras.metrics.BinaryAccuracy(
        #     name="accuracy", dtype=None, threshold=0.5
        # ),
        tf.keras.metrics.RootMeanSquaredError(
            name="rmse", dtype=None
        )
        # keras.metrics.Precision(
        #     name="precision", dtype=None, # thresholds=0.5
        # ),
    ]
)

if(path.exists('models/model_latest.h5')):
    print('Loading already-saved model (latest)...')
    model.load_weights('models/model_latest.h5')
elif(path.exists('models/model_best.h5')):
    print('Loading already-saved model (best)...')
    model.load_weights('models/model_best.h5')
elif(path.exists('models/model_saved.h5')):
    print('Loading  already-saved model...')
    model.load_weights('models/model_saved.h5')

print('Model ready')
print()

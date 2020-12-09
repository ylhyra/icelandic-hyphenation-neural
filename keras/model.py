# Originally written by Markus Siemens (MIT; https://github.com/msiemens/HypheNN-de)
# Changes by Egill

import math

import keras
import tensorflow as tf
import os.path
from os import path
import keras.backend as K
from random import randint

from config import *


# if(path.exists('models/models_latest.h5')):
#     print('Loading already-saved model (latest)...')
#     model = keras.models.load_model('models/models_latest.h5')
# elif(path.exists('models/model_best.h5')):
#     print('Loading already-saved model (best)...')
#     model = keras.models.load_model('models/model_best.h5')
# elif(path.exists('models/model_saved.h5')):
#     print('Loading  already-saved model...')
#     model = keras.models.load_model('models/model_saved.h5')
# else:
print('Building model...')

model = keras.models.Sequential()
# model.add(keras.layers.Flatten(input_shape=(
#     WINDOW_SIZE, number_of_possible_letters)))

#
model.add(keras.layers.Conv1D(
    filters=120,
    kernel_size=3,
    activation='relu',
    input_shape=(WINDOW_SIZE, number_of_possible_letters)
))
model.add(keras.layers.Conv1D(
    filters=60,
    kernel_size=4,  # A total of 6 letters at once
    activation='relu',
))
model.add(keras.layers.Conv1D(
    filters=40,
    kernel_size=6,  # A total of 11 letters at once
    activation='relu',
))
model.add(keras.layers.Conv1D(
    filters=20,
    kernel_size=1,
    activation='relu',
))
model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(100, activation='relu'))
model.add(keras.layers.Dense(100, activation='relu'))
# model.add(keras.layers.Dense(3, activation='relu'))

if __name__ == '__main__':
    model.summary()
    exit()

model.add(keras.layers.Dense(
    OUTPUT_NODES,
    activation='linear'
))


def penalize_false_positives(y_pred, y_true):
    # K.sum(K.round(K.clip(Y_true - Y_pred, 0, 1)))

    false_positives_mse = K.mean(K.square(K.clip((y_true-y_pred), 0, 1)))

    mse = K.mean(K.square(y_pred-y_true))

    out = false_positives_mse * 10 + mse
    # neg_y_true = 1 - y_true
    # neg_y_pred = 1 - y_pred
    # fp = K.sum(neg_y_true * y_pred)
    # tn = K.sum(neg_y_true * neg_y_pred)
    # specificity = tn / (tn + fp + K.epsilon())
    return out


model.compile(
    optimizer=OPTIMIZER,
    # loss=LOSS,
    loss=penalize_false_positives,
    metrics=[
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

if(path.exists('models/models_latest.h5')):
    print('Loading already-saved model (latest)...')
    model.load_weights('models/models_latest.h5')
elif(path.exists('models/model_best.h5')):
    print('Loading already-saved model (best)...')
    model.load_weights('models/model_best.h5')
elif(path.exists('models/model_saved.h5')):
    print('Loading  already-saved model...')
    model.load_weights('models/model_saved.h5')

print('Model ready')
print()

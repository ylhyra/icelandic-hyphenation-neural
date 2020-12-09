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
    filters=60,
    kernel_size=3,
    activation='relu',
    # padding='same',
    input_shape=(WINDOW_SIZE, number_of_possible_letters)
))
model.add(keras.layers.Conv1D(
    filters=60,
    kernel_size=3, # A total of 5 letters at once
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Conv1D(
    filters=40,
    kernel_size=3, # A total of 7 letters at once
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Conv1D(
    filters=20,
    kernel_size=1,
    # kernel_size=int(WINDOW_SIZE/2),
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Conv1D(
    filters=16,
    kernel_size=3, # A total of 9 letters at once
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Conv1D(
    filters=16,
    kernel_size=3,  # A total of 11 letters at once
    # kernel_size=int(WINDOW_SIZE/2),
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Conv1D(
    filters=4,
    kernel_size=1,
    # kernel_size=int(WINDOW_SIZE/2),
    activation='relu',
    # padding='same',
))
model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(10, activation='relu'))
model.add(keras.layers.Dense(3, activation='relu'))
model.add(keras.layers.Dense(3, activation='relu'))

if __name__ == '__main__':
    model.summary()
    exit()

model.add(keras.layers.Dense(
    OUTPUT_NODES,
    activation='linear'
))

model.compile(
    optimizer=OPTIMIZER,
    loss=LOSS,
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

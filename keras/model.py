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

model.add(keras.layers.Conv1D(
    filters=32,
    kernel_size=8,
    activation='relu',
    input_shape=(WINDOW_SIZE, number_of_possible_letters)
))
model.add(keras.layers.Conv1D(
    filters=14,
    kernel_size=1,
    activation='relu',
))
model.add(keras.layers.Conv1D(
    filters=3,
    kernel_size=1,
    activation='relu',
))
# model.add(keras.layers.MaxPooling1D(pool_size=2))
model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(40, activation='relu'))
model.add(keras.layers.Dense(10, activation='relu'))
# model.add(keras.layers.Dense(SECOND_LAYER_NODES, activation='relu'))

# model.add(keras.layers.Flatten(input_shape=(
#     WINDOW_SIZE, number_of_possible_letters)))
# # if CONV_LAYER:
# #     model.add(keras.layers.Conv1D(filters=256, kernel_size=5, activation='relu',input_shape=(WINDOW_SIZE * number_of_possible_letters,1)))
# if SECOND_LAYER_NODES:
#     model.add(keras.layers.Dense(SECOND_LAYER_NODES, activation='relu'))
# if THIRD_LAYER_NODES:
#     model.add(keras.layers.Dropout(0.4 * DROPOUT_LEVEL))
#     model.add(keras.layers.Dense(THIRD_LAYER_NODES, activation='relu'))
# if FOURTH_LAYER_NODES:
#     model.add(keras.layers.Dropout(0.3 * DROPOUT_LEVEL))
#     model.add(keras.layers.Dense(FOURTH_LAYER_NODES, activation='relu'))
# if FIFTH_LAYER_NODES:
#     model.add(keras.layers.Dropout(0.2 * DROPOUT_LEVEL))
#     model.add(keras.layers.Dense(FIFTH_LAYER_NODES, activation='relu'))
# if SIXTH_LAYER_NODES:
#     # model.add(keras.layers.Dropout(0.01 * DROPOUT_LEVEL))
#     model.add(keras.layers.Dense(SIXTH_LAYER_NODES, activation='relu'))

# testing
# model.add(keras.layers.Dense(400, activation='relu'))
# model.add(keras.layers.Dense(400, activation='relu'))

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

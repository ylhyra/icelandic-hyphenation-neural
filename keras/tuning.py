from tensorflow import keras
from tensorflow.keras import layers
import kerastuner
from kerastuner.tuners import RandomSearch
from train import get_batch, total_samples_in_dataset
import math
import dataset


def build_model(hp):

    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=(
        dataset.WINDOW_SIZE, dataset.number_of_possible_letters)))
    model.add(layers.Dense(units=hp.Int('units',
                                        min_value=38,
                                        max_value=150,
                                        step=15),
                           activation='relu'))
    model.add(layers.Dense(units=hp.Int('units',
                                        min_value=8,
                                        max_value=20,
                                        step=4),
                           activation='relu'))
    model.add(keras.layers.Dense(3, activation='sigmoid'))

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate',
                      values=[1e-2, 1e-3, 1e-4])),
        loss='binary_crossentropy',
        metrics=[keras.metrics.BinaryAccuracy(
            name="accuracy", dtype=None, threshold=0.5
            )]
    return model


tuner=RandomSearch(
    build_model,
    objective='accuracy',
    max_trials=5,
    executions_per_trial=1,
    directory='tuning_test',
    project_name='helloworld')

print(tuner.search_space_summary())

tuner.search(
    get_batch(),
    batch_size=512,
    steps_per_epoch=math.ceil(total_samples_in_dataset / 512),
    epochs=8,
)


best_model=tuner.get_best_models(1)[0]
best_hyperparameters=tuner.get_best_hyperparameters(1)[0]
print('Best hyperparameters:')
print(best_hyperparameters.serialize())
best_model.save('data/models_found_with_tuning.h5')

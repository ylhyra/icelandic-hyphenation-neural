# test, from https://github.com/yahiakr/KerasGA, gpl3

import numpy as np
import random

import tensorflow as tf
from model import model
from KerasGA import GeneticAlgorithm
from dataset import process_word
# from keras.utils.conv_utils import convert_kernel
# from train import get_batch
from config import *

population_size = 5
generations = 2





# for layer in model.layers:
#     for weights in layer.weights:
#         print(weights)
#         exit()
#         # if len(weights.shape) != 1 :
#         #     print(weights.shape)
# exit()


GA = GeneticAlgorithm(model, population_size=population_size,
                      selection_rate=0.1, mutation_rate=0.2,)

population = GA.initial_population()

scores = []
for chromosome in population:
    model.set_weights((chromosome))
    # # then evaluate the chromosome (i.e assign its final score)
    score = 0
    to_predict = []
    to_predict_y = []
    f = open('data/wordlist-extra-extra-small.txt')
    for line in f:
        if(len(line.strip()) >= 2):
            x_values, y_values = process_word(line.strip())
            to_predict.extend((x_values))
            to_predict_y.extend((y_values))
    f.close()

    predicted_all = model.predict(tf.convert_to_tensor((to_predict)))
    to_write = ''
    for index in range((len(to_predict_y))):
        correct = to_predict_y[index]
        predicted = predicted_all[index]

        if(correct < 0 and predicted > 0):
            score -= 50
        elif correct < -.2 and predicted < -.2:
            score += 0
        elif abs(correct - predicted) < 0.2:
            score += 1
        elif abs(correct - predicted) < 0.4:
            score += 0.1
        else:
            score -= 1

    scores.append(score)

print(scores)
# Selection:
# 'scores' is a list of length = population_size
# 'top_performers' is a list of tuples: (chromosome, it's score)
# top_performers = GA.strongest_parents(population,scores)

# # Make pairs:
# # 'GA.pair' return a tuple of type: (chromosome, it's score)
# pairs = []
# while len(pairs) != GA.population_size:
#     pairs.append( GA.pair(top_performers) )
#
# # Crossover:
# base_offsprings =  []
# for pair in pairs:
#     offsprings = GA.crossover(pair[0][0], pair[1][0])
#     # 'offsprings' contains two chromosomes
#     base_offsprings.append(offsprings[-1])
#
# # Mutation:
# new_population = GA.mutation(base_offsprings)

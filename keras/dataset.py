# Originally written by Markus Siemens (MIT; https://github.com/msiemens/HypheNN-de)
# Changes by Egill

import math
import os.path
from os import path
from random import random
from random import randint
import numpy as np
from config import *

char_to_int = {c: i for i, c in enumerate(chars)}
int_to_char = {v: k for k, v in char_to_int.items()}
int_to_char[0] = '_'


def process_data(words):
    X = []
    y = []

    for i, word in enumerate(words):
        data = process_word(word)
        X.extend(data[0])
        y.extend(data[1])

        if (i + 1) % 100 == 0:
            print('\rProcessed {} entries ({} %)'.format(
                i + 1, round((i + 1) / len(words) * 100)), end='')

    return np.asarray(X), np.asarray(y)


def process_word(word, training=True):

    # # Normalize "-" to "." when
    # if '-' in word and not '.' in word:
    #     word = word.replace('-','.')


    X = []
    y = []

    word_int = [char_to_int[c] for c in word if (
        c != MAJOR_HYPHENATION_INDICATOR and
        c != MINOR_HYPHENATION_INDICATOR and
        c != MORPHEME_BREAK_INDICATOR
    )]
    word_int = np.array(word_int)
    number_of_hyphenations_seen = 0

    # print('>>> word:', word)  # For debugging, may be removed
    # print('>>> word_int:', word_int)  # For debugging, may be removed
    # exit()

    # Minus one since we start at the second letter
    padding = np.zeros(int(WINDOW_SIZE / 2 - 1))
    word_int = np.concatenate((padding, word_int, padding)).astype(int)

    # Calculate the number of times we have to slide the window to cover
    # the whole word
    num_windows = len(word_int) - WINDOW_SIZE + 1
    indexer = np.arange(WINDOW_SIZE)[None, :] + np.arange(num_windows)[:, None]
    windows = word_int[indexer]

    # print('>>> num_windows:', num_windows)# For debugging, may be removed
    # exit()

    # Calculate hyphenation positions
    for offset, window in enumerate(windows):

        # For debugging, may be removed
        _w = ''.join([int_to_char[c] for c in window])
        # print('>>> offset:', offset)  # For debugging, may be removed
        # print('>>> window:', window)  # For debugging, may be removed
        # print('>>> word:', _w[0:int(WINDOW_SIZE/2)], _w[int(WINDOW_SIZE/2):])  # For debugging, may be removed

        # print('>>> o:', word[o])

        if training:
            next_character = word[
                offset + number_of_hyphenations_seen + 1  # + 1 to check next char
            ]
            y_value = -1
            if(next_character == MAJOR_HYPHENATION_INDICATOR):
                y_value = MAJOR_HYPHENATION_INDICATOR_VALUE
            elif(next_character == MINOR_HYPHENATION_INDICATOR):
                y_value = MINOR_HYPHENATION_INDICATOR_VALUE
            elif(next_character == MORPHEME_BREAK_INDICATOR):
                y_value = MORPHEME_BREAK_INDICATOR_VALUE
            if y_value > 0:
                number_of_hyphenations_seen += 1

        # _c += _w[4]  # For debugging, may be removed
        #
        # print('>>> c:', word[o])  # For debugging, may be removed
        # print('>>> _c:', _c, _w[4])  # For debugging, may be removed
        # print('>>> h:', hyphenation) # For debugging, may be removed
        # np.array(
        #     major_hyphenation,
        #     minor_hyphenation,
        #     morpheme_break,
        # )
        # print(window)
        # exit()

        one_hot = np.zeros(
            (int(WINDOW_SIZE), number_of_possible_letters), dtype=np.bool)

        # Add random noise to sides
        if training and NOISE_LEVEL_AT_WORD_EDGES:
            if(window[0] and random() < 0.6 * NOISE_LEVEL_AT_WORD_EDGES):
                window[0] = randint(0, number_of_possible_letters - 1)
            if(window[1] and random() < 0.4 * NOISE_LEVEL_AT_WORD_EDGES):
                window[1] = randint(0, number_of_possible_letters - 1)
            if(window[2] and random() < 0.05 * NOISE_LEVEL_AT_WORD_EDGES):
                window[2] = randint(0, number_of_possible_letters - 1)
            # if(window[3] and randint(0, 10) > 9):
            #     window[3] = randint(0, number_of_possible_letters - 1)
            # if(window[WINDOW_SIZE - 4] and randint(0, 10) > 9):
            #     window[WINDOW_SIZE - 4] = randint(0, number_of_possible_letters - 1)
            if(window[WINDOW_SIZE - 3] and random() < 0.05 * NOISE_LEVEL_AT_WORD_EDGES):
                window[WINDOW_SIZE -
                       3] = randint(0, number_of_possible_letters - 1)
            if(window[WINDOW_SIZE - 2] and random() < 0.4 * NOISE_LEVEL_AT_WORD_EDGES):
                window[WINDOW_SIZE -
                       2] = randint(0, number_of_possible_letters - 1)
            if(window[WINDOW_SIZE - 1] and random() < 0.6 * NOISE_LEVEL_AT_WORD_EDGES):
                window[WINDOW_SIZE -
                       1] = randint(0, number_of_possible_letters - 1)

        one_hot[np.arange(int(WINDOW_SIZE)), window] = True
        X.append(one_hot)

        if training:
            # output = np.array([
            #     major_hyphenation,
            #     minor_hyphenation,
            #     morpheme_break,
            #     # no_break: not (major_hyphenation or minor_hyphenation or morpheme_break),
            # ])
            # # print(output)
            # y.append(output)
            y.append(y_value)

    if training:
        return X, y
    else:
        return X


if __name__ == '__main__':
    print("Total Vocab: ", number_of_possible_letters)
    print("Characters:", chars)

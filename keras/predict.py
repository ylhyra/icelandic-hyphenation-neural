# Originally written by Markus Siemens (MIT; https://github.com/msiemens/HypheNN-de)
# Changes by Egill

import sys

import numpy as np
from config import *
import dataset
from model import model

# .backend.set_learning_phase(0)

def predict(word, model):
    windows = dataset.process_word(word.lower(), training=False)
    predicted = model.predict(np.array(windows))
    out = ''
    for index, char in enumerate(word):
        out += char
        if index + 1 < len(predicted):
            # print('char: ' + char + ' val:' + str(predicted[index][0]))
            # print(predicted[index])
            if predicted[index][0] > MAJOR_HYPHENATION_INDICATOR_VALUE - 0.2:
                out += '\033[91m'+MAJOR_HYPHENATION_INDICATOR+'\033[0m'
            elif predicted[index][0] > MINOR_HYPHENATION_INDICATOR_VALUE - 0.2:
                out += '\033[91m'+MINOR_HYPHENATION_INDICATOR+'\033[0m'
            elif predicted[index][0] > MORPHEME_BREAK_INDICATOR_VALUE - 0.15:
                out += '\033[91m'+MORPHEME_BREAK_INDICATOR+'\033[0m'
            if(predicted[index][0] > 0):
                out += '\033[91m'+str(int(round(predicted[index][0] * 10)))+'\033[0m'
    return out


if __name__ == '__main__':
    word = sys.argv[1]
    prediction = predict(word, model)
    print('Input:', word)
    print('Hyphenation:', prediction)

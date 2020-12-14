import re
import dataset
from model import model
import numpy as np
from config import *

BATCH_SIZE = 10000
count = 0
to_write = ''
f = open('list_tmp.txt')
total_samples = sum(1 for line in open('list_tmp.txt'))
words_in_memory = []
to_predict = []
current_index_in_prediction = 0
for line in f:
    word = line.strip()
    words_in_memory.append(word)

    if(len(word) >= 4 and re.search('^[abcdefghijklmnoprstuvwxyzáæéíðóöúýþ]+?$', word)):
        to_predict = to_predict + dataset.process_word(word, training=False)
    count = count + 1
    if(count % BATCH_SIZE == 0 or count == total_samples):
        predicted = model.predict(np.array(to_predict))
        to_write = ''
        for _word in words_in_memory:
            out = ""
            if(len(_word) >= 4 and re.search('^[abcdefghijklmnoprstuvwxyzáæéíðóöúýþ]+?$', _word)):
                for index, char in enumerate(_word):
                    out += char
                    if index + 1 < len(_word):
                        if predicted[current_index_in_prediction][0] > 0.9:
                            out += '9'
                        elif predicted[current_index_in_prediction][0] > 0.8:
                            out += '8'
                        elif predicted[current_index_in_prediction][0] > 0.6:
                            out += '6'
                        elif predicted[current_index_in_prediction][0] > 0.4:
                            out += '4'
                        elif predicted[current_index_in_prediction][0] > 0.3:
                            out += '3'
                        elif predicted[current_index_in_prediction][0] > 0.2:
                            out += '2'
                        elif predicted[current_index_in_prediction][0] > -0.1:
                            out += '0'
                        # if predicted[current_index_in_prediction][0] > MAJOR_HYPHENATION_INDICATOR_VALUE - 0.3:
                        #     out += dataset.MAJOR_HYPHENATION_INDICATOR
                        # elif predicted[current_index_in_prediction][0] > MINOR_HYPHENATION_INDICATOR_VALUE - 0.1:
                        #     out += dataset.MINOR_HYPHENATION_INDICATOR
                        # elif predicted[current_index_in_prediction][0] >  MORPHEME_BREAK_INDICATOR_VALUE - 0.1:
                        #     out += dataset.MORPHEME_BREAK_INDICATOR
                        current_index_in_prediction = current_index_in_prediction + 1
            else:
                out = _word
            to_write += out + "\n"

        print(count)
        with open("list_tmp_output.txt", "a") as myfile:
            myfile.write(to_write)
        # exit()
        words_in_memory = []
        to_predict = []
        current_index_in_prediction = 0
f.close()

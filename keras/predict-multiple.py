import dataset
from model import model
import numpy as np

BATCH_SIZE = 5000
count = 0
to_write = ''
f = open('data/random_icelandic_sentences.txt')
words_in_memory = []
to_predict = []
current_index_in_prediction = 0
for line in f:
    word = line.strip()
    words_in_memory.append(word)
    if(len(word) >= 4):
        to_predict = to_predict + dataset.process_word(word, training=False)
    count = count + 1
    if(count % BATCH_SIZE == 0):
        predicted = model.predict(np.array(to_predict))
        to_write = ''
        for _word in words_in_memory:
            out = ""
            if(len(_word) >= 4):
                for index, char in enumerate(_word):
                    out += char
                    if index + 1 < len(_word):
                        if predicted[current_index_in_prediction][0] > 0.5:
                            out += dataset.MAJOR_HYPHENATION_INDICATOR
                        elif predicted[current_index_in_prediction][1] > 0.5:
                            out += dataset.MINOR_HYPHENATION_INDICATOR
                        elif predicted[current_index_in_prediction][2] > 0.5:
                            out += dataset.MORPHEME_BREAK_INDICATOR
                        current_index_in_prediction = current_index_in_prediction + 1
            else:
                out = _word
            to_write += out + "\n"

        print(count)
        with open("data/random_icelandic_sentences_output.txt", "a") as myfile:
            myfile.write(to_write)
        # exit()
        words_in_memory = []
        to_predict = []
        current_index_in_prediction = 0
f.close()

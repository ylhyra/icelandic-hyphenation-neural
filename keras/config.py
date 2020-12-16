import keras
import tensorflow as tf

# Data config
# Must start with an empty value
chars = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'á', 'æ', 'é', 'í', 'ð', 'ó', 'ö', 'ú', 'ý', 'þ']
number_of_possible_letters = len(chars)
WINDOW_SIZE = 22 # Must be an even number
MAJOR_HYPHENATION_INDICATOR = '-'
MINOR_HYPHENATION_INDICATOR = '.'
MORPHEME_BREAK_INDICATOR = '|'
MAJOR_HYPHENATION_INDICATOR_VALUE = 1.0
MINOR_HYPHENATION_INDICATOR_VALUE = 0.55
MORPHEME_BREAK_INDICATOR_VALUE = 0.1
# TEMP!!
# MINOR_HYPHENATION_INDICATOR_VALUE = 1.0
# MORPHEME_BREAK_INDICATOR_VALUE = 1.0

# Training data

TRAINING_SET = 0

if(TRAINING_SET == 0):
    FILE = 'data/wordlist.txt'
    VALIDATION_FILE = 'data/validation-full.txt'
if(TRAINING_SET == 1):
    FILE = 'data/wordlist-small.txt'
    VALIDATION_FILE = 'data/validation-from-extra-small.txt'
if(TRAINING_SET == 2):
    FILE = 'data/wordlist-extra-small.txt'
    VALIDATION_FILE = 'data/validation-from-extra-small.txt'
if(TRAINING_SET == 3):
    FILE = 'data/wordlist-extra-extra-small.txt'
    VALIDATION_FILE = 'data/wordlist-extra-extra-small.txt'
# Full data without junk data
if(TRAINING_SET == 4):
    FILE = 'data/wordlist-real.txt'
    VALIDATION_FILE = 'data/validation-from-extra-small.txt'

LOSS='mse'
# LOSS='binary_crossentropy'
OPTIMIZER='adam'
# OPTIMIZER=keras.optimizers.Adam(learning_rate=1E-4)
# OPTIMIZER=keras.optimizers.Adam(learning_rate=5E-5)
# OPTIMIZER=keras.optimizers.Adam(learning_rate=1E-5)
# OPTIMIZER=keras.optimizers.Adam(learning_rate=5E-6)
# OPTIMIZER=keras.optimizers.Adam(learning_rate=1E-6)


# Noise & dropout

DROPOUT_LEVEL = 0#.3#.2 # Range from 0 to 1
NOISE_LEVEL_AT_WORD_EDGES = 0#.1#.3

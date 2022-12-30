#==============================================================================#
# Imports
import os
from constants import *

def load_raw_freq_data():
    with open("frequency_data.dat", 'r') as file:
        return {line.split(' ')[0]: int(line.split(' ')[1]) for line in file}

def load_frequent_words():
    with open(FREQUENT_FNAME, 'r') as file:
        words = [line.strip() for line in file]
    return set(words)

if __name__ == "__main__":
    words = dict()
    with open("frequency_data.dat", 'r') as file:
        lines = [line for line in file]

    for line in lines:
        w, f = line.split(' ')
        if int(f) >= FREQUENCY_CUTOFF:
            words[w] = int(f)

    if os.path.exists(FREQUENT_FNAME):
        os.remove(FREQUENT_FNAME)
    with open(FREQUENT_FNAME, 'w') as file:
        [file.write(f"{w}\n") for w in words.keys()]

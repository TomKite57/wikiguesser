#==============================================================================#
# Imports
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
# My files
from frequency_handler import load_frequent_words, load_raw_freq_data
from utility import string_distance
from constants import *

#==============================================================================#
# Tokenize
def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    return tokens

#==============================================================================#
# Filters
def filter_stopwords_words(tokens):
    tokens = [token for token in tokens if token not in set(stopwords.words('english'))]
    return tokens

def filter_common_words(tokens):
    common = load_frequent_words()
    tokens = [token for token in tokens if token not in common]
    return tokens

def filter_punctuation(tokens):
    punctuation = set(string.punctuation)
    tokens = [token for token in tokens if token not in punctuation]
    return tokens

def filter_custom(tokens, *args):
    custom = set(args)
    tokens = [token for token in tokens if token not in custom]
    return tokens

def filter_length(tokens, n=1):
    tokens = [token for token in tokens if len(token) > n]
    return tokens

def filter_numbers(tokens):
    tokens = [token for token in tokens if not token.isdigit()]
    return tokens

def filter_title_words(tokens, title):
    for t in title.split(' '):
        tokens = [token for token in tokens if string_distance(token, t.lower())>2]
    return tokens

def apply_all_filters(tokens, title):
    tokens = filter_stopwords_words(tokens)
    tokens = filter_common_words(tokens)
    tokens = filter_numbers(tokens)
    tokens = filter_punctuation(tokens)
    tokens = filter_length(tokens)
    tokens = filter_custom(tokens, *CUSTOM_TOKENS)
    tokens = filter_title_words(tokens, title)
    return tokens

#==============================================================================#
# Orderings
def frequency_ordering(tokens):
    rval = []
    fdist = FreqDist(tokens)
    for word, count in fdist.most_common(10):
        rval.append(word)
    rval = sorted(rval, key=lambda w: fdist[w], reverse=True)
    return rval

def uncommon_ordering(tokens):
    rval = []
    fdist = FreqDist(tokens)
    for word, count in fdist.most_common(15):
        if count == 1:
            break
        rval.append(word)

    freq_data = load_raw_freq_data()
    rval = sorted(rval, key = lambda w: freq_data.get(w, 0))
    return rval[:10]

#==============================================================================#
# All together now
def all_filters_and_frequency(text, title):
    tokens = tokenize_text(text)
    tokens = apply_all_filters(tokens, title)
    return uncommon_ordering(tokens)

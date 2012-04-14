#!/usr/env/python

import random

import redis

from letter_probabilities import LetterCounts
from word_generation import MarkovChainObject


def quasi_random_next(chain):
    """Given a Markov Chain of probabilities, pick a 
    random number and choose the corresponding letter
    from the chain's probability ranges"""
    r = random.random()
    letters = []
    [letters.append(key[0]) for key in chain.keys() if key[0] not in letters]
    for letter in letters:
        lower = float(chain["%s:low" % letter])
        upper = float(chain["%s:high" % letter])
        if lower < r < upper:
            return letter

def word_given_seed_and_length(seed, length, redis_instance):
    """Given a redis instance, an initial state(letter) and 
    a length, output the next state(letter) using the 
    Markov Chains in the redis instance"""
    current_chain = redis_instance.hgetall(seed)
    letters = [seed]
    last = seed
    for i in xrange(length - 1):
        current_letter = quasi_random_next(current_chain)
        letters.append(current_letter)
        last = current_letter
        current_chain = redis_instance.hgetall(last)
    return ''.join(letters)

    
if __name__ == '__main__':
    import sys
    words = open("/usr/share/dict/words", 'rb')
    letter_counts = LetterCounts(words)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    chain_list = []
    for state, chains in letter_counts.ranges.iteritems():
        for candidate, prob_range in chains.iteritems():
            low = str(prob_range[0])
            high = str(prob_range[1])
            r.hset(state, "%s:low" % candidate, "%s" % low)
            r.hset(state, "%s:high" % candidate, "%s" % high)
    ERROR = False
    while True:
        if not ERROR:
            message = "Enter a first <letter> <space> and a length <integer>:\n> "
        else:
            message = "\n\nSorry! Enter a single letter followed by a space and an integer.\n> "
            ERROR = False
        try:
            values = raw_input(message)
            seed, length = values.split(" ")
            print(word_given_seed_and_length(seed, int(length), r))
            print('')

        except ValueError:
            ERROR = True



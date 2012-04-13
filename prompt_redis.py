import random
import string

from letter_probabilities import LetterCounts
from word_generation import MarkovChainObject
import redis

""" >>> import redis
    >>> r = redis.StrictRedis(host='localhost', port=6379, db=0)
    >>> r.set('foo', 'bar')
    True
    >>> r.get('foo')
    'bar'

"""

def quasi_random_next(chain):
    qr = random.random()
    candidate = None
################################################################################

    for key in chain.iteritems():
        lower = float(chain["%s:low" % key])
        upper = float(chain["%s:high" % key])
        if lower < qr < upper:
            candidate = c
    return candidate

def word_given_seed_and_length(seed, length, redis_instance):

    # returns a dict of all key values
    current_chain = redis_instance.hgetall(seed)

    letters = [seed]
    last = seed
    for i in xrange(length - 1):
        current_letter = quasi_random_next(current_chain)
        letters.append(current_letter)
        last = current_letter
    return ''.join(letters)

    
if __name__ == '__main__':
    import sys
    words = open("/usr/share/dict/words", 'rb')
    letter_counts = LetterCounts(words)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # data structure: 
    # HSET z a:low "0"
    # HSET z a:high "1995795721528379"
    # HSET z c:low "1995795721528379"
    # HSET z c:high "20069246939532584"
    chain_list = []
    for state, chains in letter_counts.ranges.iteritems():
        # chain_list.append(MarkovChainObject(candidate, chains))
        for candidate, prob_range in chains.iteritems():
            print("candidate: %s state: %s range: %s" % (state, candidate, prob_range))
            low = str(prob_range[0])
            high = str(prob_range[1])
            r.hset(state, "%s:low" % candidate, "%s" % low)
            r.hset(state, "%s:high" % candidate, "%s" % high)
        
    while True:
        values = raw_input("Enter a first <letter> <space> and a length <integer>:\n> ")
        seed, length = values.split(" ")
        print(word_given_seed_and_length(seed, int(length), r))
    
    



import collections
import random
import string

from letter_probabilities import LetterCounts

class MarkovChainObject(object):
    """self.current is represents a current state. self.chains
    represents a list of `next` states and an associated normalized range of 
    values that span the probability of the `next` object following 
    
    example: self.current = 'a'
             self.chains = [{'b': (0, .03), 'c': (.03, .53), 'd': (.53, 1)}]
    """
    
    def __init__(self, current, chain):
        self.current = current
        self.chain = chain

    def quasi_random_next(self):
        qr = random.random()
        candidate = None

        for c in self.chain:

            lower = self.chain[c][0]
            upper = self.chain[c][1]
            if lower < qr < upper:
                candidate = c
        return candidate


class GenerateQuasiRandomWord(object):
    """Given a list of MarkovChainObjects, create a word 
    with the chains. 
    """
    def __init__(self, chains):
        self.chains = chains
        self.chain_table = collections.defaultdict(dict)
        self._index_chain_table()

    def _index_chain_table(self):
        """create dictionary- the key is the seed letter and the
        value is the MarkovChainObject associated with that letter"""
        for letter in string.lowercase:
            for chain in self.chains:
                if chain.current == letter:
                    self.chain_table[letter] = chain

    def word_given_seed_and_length(self, seed, length):
        letters = [seed]
        last = seed
        for i in xrange(length - 1):
            current_letter = self.chain_table[last].quasi_random_next()
            letters.append(current_letter)
            last = current_letter
        return ''.join(letters)


if __name__ == '__main__':
    import sys
    words = open("/usr/share/dict/words", 'rb')
    letter_counts = LetterCounts(words)
    chain_list = []
    for candidate, next_candidate in letter_counts.ranges.iteritems():
        # print candidate, next_candidate
        chain_list.append(MarkovChainObject(candidate, next_candidate))
    quasi_generator = GenerateQuasiRandomWord(chain_list)

    print(quasi_generator.word_given_seed_and_length(sys.argv[1].lower(), int(sys.argv[2])))

    



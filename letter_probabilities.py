#!/usr/env/python
import collections
import string


class LetterCounts(object):
    """Generate probabilities of next characters, given an iterable of words"""
    def __init__(self, iterable):
        self.iterable = iterable
        self.lengths = collections.defaultdict(int)
        self.pair_counter = collections.defaultdict(lambda:collections.defaultdict(int))
        self.pair_probabilities = collections.defaultdict(lambda:collections.defaultdict(float))
        self.ranges = collections.defaultdict(lambda:collections.defaultdict(tuple))

        self.count_consecutive_letters()
        self.generate_probabilities()
        self.generate_ranges()

    def count_consecutive_letters(self):
        """ for each word, acquire the count of all consecutive letter pairs
        permutations and the lengths of all items within self.iterable"""
        for word in self.iterable:
            self.lengths[len(word)] += 1
            last_letter = word[0]
            for letter in word[1:].lower():
                if letter not in (None, '\n', '\t' , ' '):
                    self.pair_counter[last_letter][letter] += 1
                    last_letter = letter 
        return self.pair_counter

    def generate_probabilities(self):
        """ for each lowercase letter, create a list of objects; the key is the 
        next letter and the value is a tuple of a range between 0 and 1 ( actually .9999999999999 )"""
        sums = {}
        key_sums = [sums.update({k:sum(v.values())}) for k,v in self.pair_counter.iteritems()]
        for k, v in self.pair_counter.iteritems():
            for key, value in v.iteritems():
                self.pair_probabilities[k][key] = float(value)/sums[k]

    def generate_ranges(self):
        """Generate a dictionary of dictionaries containing tuples of incremental sums of probabilities 
        ( ie a Markov Chain )"""
        for key, probabilities, in self.pair_probabilities.iteritems():
            last_value = 0
            for k, value in probabilities.iteritems():
                self.ranges[key][k] = (last_value, value + last_value)
                last_value += value

if __name__ == "__main__":
    words = open("/usr/share/dict/words", 'rb')
    letter_counts = LetterCounts(words)
    for letter, next_letter_obj in letter_counts.ranges.iteritems():
        print("letter:\n    %s\nnext letter probability range:\n    %s\n" % (letter, next_letter_obj))


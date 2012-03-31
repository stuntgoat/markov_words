
import collections
import string


class LetterCounts(object):
    def __init__(self, iterable):
        self.iterable = iterable
        self.lengths = collections.defaultdict(int)
        self.pair_counter = collections.defaultdict(int)
        self.single_letter_sets = collections.defaultdict(list)
        self.single_letter_probability = collections.defaultdict(list)
        self.single_letter_ranges = collections.defaultdict(list)
        self.chain_list = []

    def count_consecutive_letters(self):
        """ for each word, acquire the count of all consecutive letter 
        permutations within self.iterable"""

        for word in self.iterable:
            split_word = list(word.lower())
            last_letter = None
            # acquire lengths of all words
            self.lengths[len(split_word)] += 1
            for letter in split_word:
                if letter not in string.lowercase:
                    continue
                try:
                    if last_letter != None:
                        self.pair_counter[last_letter + letter] += 1
                        last_letter = letter
                    else:
                        last_letter = letter
                except Error as e:
                    print e
            
    def create_single_letter_sets(self):
        """ for each lowercase letter, create a list of objects, where the key is 
        the letter pair and the value is the consecutive occurance in each
        item in self.iterable"""

        for letter in string.lowercase:
            for pair in self.pair_counter:
                if pair[0] == letter:
                    self.single_letter_sets[letter].append({pair: self.pair_counter[pair]})
  
    def generate_probabilities(self):
        """for each letter create a list of objects; the key is that letter and
        value is a float of the probability of moving to that letter"""
        total = 0
        for letter, values in self.single_letter_sets.iteritems():
            for obj in values:
                total += obj.values()[0]
            for obj in values:
                key = obj.keys()[0]
                self.single_letter_probability[letter].append({key[1]: (obj.values()[0]/float(total))})
            total = 0
        
    def generate_ranges(self):
        """ for each lowercase letter, create a list of objects; the key is the next letter and the value is a tuple of a range between 0 and 1 ( actually .9999999999999 )"""
        last = 0
        for letter, letter_set in self.single_letter_probability.iteritems():
            for obj in letter_set:
                current_value = obj.values()[0]
                self.single_letter_ranges[letter].append({obj.keys()[0]:(last, current_value + last)})
                last += current_value
            last = 0


if __name__ == "__main__":
    words = open("/usr/share/dict/words", 'rb')
    letter_counts = LetterCounts(words)
    letter_counts.count_consecutive_letters()
    letter_counts.create_single_letter_sets()
    letter_counts.generate_probabilities()
    letter_counts.generate_ranges()
    for letter, next_letter_obj in letter_counts.single_letter_ranges.iteritems():
        print("letter:\n    %s\nnext letter probability range:\n    %s\n" % (letter, next_letter_obj))



    

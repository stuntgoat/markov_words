**MarkovWords!!**

Create new words and fool your friends!! Free!!

Generate a quasi-random word given a first letter and a length.

     $ python word_generation.py e 7
     eaentit
     $ python word_generation.py l 6
     lyplee	     
     $ python word_generation.py z 10
     zekeroncku
    
`letter_probabilities.py` reads an iterable of words to generate Markov Chains of 'next consecutive letter' probabilities, based on the letter following each letter in every word. `word_generation.py` supplies a `MarkovChainObject` and a `GenerateQuasiRandomWord` object. The latter contains a `word_given_seed_and_length()` method that accepts a letter and a length.

These scripts were created to give me a better understanding of Markov Chains.

NEW!!
Now with a prompt that stores the chains in memory using [Redis](http://http://redis.io/ "Redis is an open source, advanced key-value store.")! ( and [redis-py](https://github.com/andymccurdy/redis-py "The Python interface to the Redis key-value store.") )

    $ python markov_words/prompt_redis.py
    Enter a first <letter> <space> and a length <integer>:
    > a 9
    aerrobire

    Enter a first <letter> <space> and a length <integer>:
    > f 13
    ficoglulomero


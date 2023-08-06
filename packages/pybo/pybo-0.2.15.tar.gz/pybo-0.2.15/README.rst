|Build Status| |Coverage Status|

Overview
--------

pybo is a word tokenizer for the Tibetan language entirely written in
Python. pybo takes in chuncks of text, and returns lists of words. It
provides an easy-to-use, high-performance tokenization pipeline that can
be adapted either as a stand-alone solution or compliment.

Getting Started
---------------

::

    pip install pybo

Or if you for some reason want to install from the latest Master branch:

::

    pip install git+https://github.com/Esukhia/pybo.git

Use
---

To initiate the tokenizer together with part-of-speech capability:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # initialize the tokenizer
    pybo = bo.BoTokenizer('POS')

    # read in some Tibetan text
    input_str = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

    # run the tokenizer
    tokens = tok.tokenize(input_str)

Now in 'tokens' you have an iterable where each token consist of several meta-data:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # access the first token in the iterable
    tokens[0]

This will yield:

::

    content: "༄༅། "
    char_types: |punct|punct|punct|space|
    type: punct
    start: 0
    len: 4
    syls: None
    tag: punct
    pos: punct
    skr: "False"
    freq: 0

notes: - ``start`` is the starting index of the current token in the
input string. - ``syls`` is a list of cleaned syllables, each syllable
being represented as a list of indices. Each index leads to a
constituting character within the input string.

In case you want to access all words in a list:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # iterate through the tokens object to get all the words in a list
    [t.content for t in tokens]

Or just get all the nouns that were used in the text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # extract nouns from the tokens
    [t.content for t in tokens if t.tag == 'NOUNᛃᛃᛃ']

These examples highlight the basic principle of accessing attributes
within each token object.

.. |Build Status| image:: https://travis-ci.org/Esukhia/pybo.svg?branch=master
   :target: https://travis-ci.org/Esukhia/pybo
.. |Coverage Status| image:: https://coveralls.io/repos/github/Esukhia/pybo/badge.svg?branch=master
   :target: https://coveralls.io/github/Esukhia/pybo?branch=master

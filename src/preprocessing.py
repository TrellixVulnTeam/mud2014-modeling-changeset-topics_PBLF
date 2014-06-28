#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

"""
Code for splitting the terms.
"""

from __future__ import print_function

import sys
import re
import string

import nltk


tokenize = nltk.word_tokenize

def to_unicode(document, info=[]):
    document = document.replace('\x00', ' ') #remove nulls
    document = document.strip()
    if not isinstance(document, unicode):
        for codec in ['utf8', 'latin1', 'ascii']:
            try:
                return unicode(document, encoding=codec)
            except UnicodeDecodeError as e:
                #logger.debug('%s %s %s' %(codec, str(e), ' '.join(info)))
                print('%s %s %s' %(codec, str(e), ' '.join(info)), file=sys.stderr)

    return document

def split(iterator):
    for token in iterator:
        word = u''
        for char in token:
            if char.isupper() and all(map(lambda x: x.isupper(), word)):
                # keep building if word is currently all uppercase
                word += char

            elif char.islower() and all(map(lambda x: x.isupper(), word)):
                # stop building if word is currently all uppercase,
                # but be sure to take the first letter back
                if len(word) > 1:
                    yield word[:-1]
                    word = word[-1]

                word += char

            elif char.islower() and any(map(lambda x: x.islower(), word)):
                # keep building if the word is has any lowercase
                # (word came from above case)
                word += char

            elif char.isdigit() and all(map(lambda x: x.isdigit(), word)):
                # keep building if all of the word is a digit so far
                word += char

            elif char in string.punctuation:
                if len(word) > 0:
                    yield word
                    word = u''

                # always yield punctuation as a single token
                yield char

            else:
                if len(word) > 0:
                    yield word

                word = char

        if len(word) > 0:
            yield word

def remove_stops(iterator, stopwords=[]):
    stopwords.extend(string.punctuation)
    stopwords.extend(string.digits)
    stopwords.extend(string.whitespace)
    for word in iterator:
        if word not in stopwords and len(word) > 0:
            try:
                int(word)
                float(word)
            except ValueError:
                yield word

def read_stops(l):
    stops = list()
    for each in l:
        with open(each) as f:
            stops.extend(f.readlines())

    return [word.strip() for word in stops]

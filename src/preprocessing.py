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

import re, string


def split(iterator, case = True, underscores = True, hyphens = True, numbers = True, symbols = True):
    splitted = []
    for i in range(len(iterator)):
        last_char = 0
        for j in range(len(iterator[i])):
            if(case):
                # does not handle case when all letters are capital
                if(iterator[i][j].isupper()):
                    if iterator[i][last_char:j] != "":
                        splitted.append(iterator[i][last_char:j])
                    last_char = j
                    continue
            if(underscores):
                if(iterator[i][j] == "_"):
                    if iterator[i][last_char:j] != '':
                        splitted.append(iterator[i][last_char:j])
                    last_char = j+1
                    continue
            if(hyphens):
                if(iterator[i][j] == "-"):
                    if iterator[i][last_char:j] != '':
                        splitted.append(iterator[i][last_char:j])
                    last_char = j+1
                    continue
            if(numbers):
                if(iterator[i][j] in "0123456789"):
                    if iterator[i][last_char:j] != '':
                        splitted.append(iterator[i][last_char:j])
                    last_char = j+1
                    continue
        if iterator[i][last_char:] != "":
            splitted.append(iterator[i][last_char:])
    return splitted


def remove_stops(iterator, stopwords):
    filtered_words = []
    for word in iterator:
        word = str(word)
        filtered_w = re.sub('[%s]' % re.escape(string.punctuation), '', word)
        if filtered_w not in stopwords:
            filtered_words.append(filtered_w)
    return filtered_words



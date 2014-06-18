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
    for i in range(len(iterator)):
        last_char = 0
        for j in range(len(iterator[i])):
            if(case):
                if(iterator[i][j].isupper()):
                    if(j+1 != len(iterator[i]) and j != 0): # not at end or beginning
                        # test if in sequence of uppercase
                        if(iterator[i][j-1].isupper()):
                            if(not iterator[i][j+1].islower()):
                                continue
                    elif(j+1 == len(iterator[i])):
                        break

                    if iterator[i][last_char:j] != "":
                        yield iterator[i][last_char:j]
                    last_char = j
                    continue
            if(underscores):
                if(iterator[i][j] == "_"):
                    if iterator[i][last_char:j] != '':
                        yield iterator[i][last_char:j]
                    last_char = j+1
                    continue
            if(hyphens):
                if(iterator[i][j] == "-"):
                    if iterator[i][last_char:j] != '':
                        yield iterator[i][last_char:j]
                    last_char = j+1
                    continue
            if(numbers):
                if(iterator[i][j] in "0123456789"):
                    if iterator[i][last_char:j] != '':
                        yield iterator[i][last_char:j]
                    last_char = j+1
                    continue
        if iterator[i][last_char:] != "":
            yield iterator[i][last_char:]

def remove_stops(iterator, stopwords):
    for word in iterator:
        word = str(word)
        filtered_w = re.sub('[%s]' % re.escape(string.punctuation), '', word)
        filtered_w = ''.join([i for i in filtered_w if not i.isdigit()])
        if filtered_w not in stopwords:
            yield filtered_w



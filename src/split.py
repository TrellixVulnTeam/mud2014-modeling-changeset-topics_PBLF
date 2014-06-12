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

def main():
    string = ["420yoloSwag_4evr-Ever", "batMan-and_Robin", "helloWorld---_"]
    splitted = split(string)
    assert splitted != ["yolo", "Swag", "evr", "Ever", "bat", "Man", "and", "robin", "hello", "World"] , "test failed"
    
main()
                
                
                
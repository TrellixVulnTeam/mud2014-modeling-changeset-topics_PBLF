#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

"""
Code for generating the corpora.
"""

from __future__ import print_function
from io import StringIO

def read_in_files(): 
    path = '/Users/kellykashuda/REU/topic-of-change/data/ant_files.txt' 
    # or
    #path = '../data/ant_files.txt' 
    list_of_files = [] 
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            stuff = '../data/' + stripped
            list_of_files.append(stuff) 
    print(list_of_files[0:3])

def read_fname(lyst, fname_out):
    with open(fname_out, 'w') as g:
        for fname in lyst:
            with open(fname, 'r') as f:
                generate_docs(fname, f, g)

def generate_docs(fname, infile, outfile):
    outfile.write(fname + " en")
    for line in infile:
        line = line.strip().split()
        for word in line:
            outfile.write(" ")
            outfile.write(word)
    outfile.write('\n')

def test_generate():
    fname = "butts.txt"
    expected = "butts.txt en burgers cats dogs hotdogs"
    with StringIO("burgers\ncats\ndogs hotdogs\n") as i:
        with StringIO() as o:
            generate_docs(fname, i, o)
            result = o.getvalue()

    assert result == expected

    i = "burgers\ncats\ndogs hotdogs\n".splitlines()
    with StringIO() as o:
        generate_docs(fname, i, o)
        result = o.getvalue()

    assert result == expected


    

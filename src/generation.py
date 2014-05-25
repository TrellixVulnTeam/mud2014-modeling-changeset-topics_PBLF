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
import os

import gensim

class MultiTextCorpus(gensim.corpora.TextCorpus):
    """ Iterates over all files within `top_dir`, yielding each file as
    a document and the fully qualified name of the file as the metadata.

    """

    def __init__(self, top_dir):
        # set top_dir first so get_texts doesn't get lost during TextCorpus.__init__
        self.top_dir = top_dir
        super(MultiTextCorpus, self).__init__()

    def get_texts(self, filter_by=lambda x: True):
        self.length = 0

        for root, dirs, files in os.walk(self.top_dir):
            # walk all files and subdirectories, yielding the contents of each
            for fname in filter(filter_by, files):
                fpath = os.path.join(root, fname)
                self.length += 1

                with open(fpath) as f:
                    document = f.read()

                if self.metadata:
                    yield gensim.utils.tokenize(document, lower=True), (fpath,)
                else:
                    yield gensim.utils.tokenize(document, lower=True)


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
        line = unicode(line)
        line = line.strip().split()
        for word in line:
            outfile.write(u" ")
            outfile.write(word)
    outfile.write(u'\n')



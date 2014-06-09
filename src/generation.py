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
import dulwich.repo

class MultiTextCorpus(gensim.corpora.TextCorpus):
    """ Iterates over all files within `top_dir`, yielding each file as
    a document and the fully qualified name of the file as the metadata.

    """

    def __init__(self, top_dir):
        # set top_dir first so get_texts doesn't get lost during TextCorpus.__init__
        self.top_dir = top_dir

        # giving it top_dir doesn't matter;
        # just forces TextCorpus to build a dictionary so docs aren't garbage
        # might be worthwhile to build the dictionary within get_texts
        super(MultiTextCorpus, self).__init__(top_dir)

    def get_texts(self):
        self.length = 0

        for root, dirs, files in os.walk(self.top_dir):
            # walk all files and subdirectories, yielding the contents of each
            for fname in files:
                fpath = os.path.join(root, fname)
                self.length += 1

                with open(fpath) as f:
                    document = f.read()

                if self.metadata:
                    yield gensim.utils.tokenize(document, lower=True), (fpath, u'en')
                else:
                    yield gensim.utils.tokenize(document, lower=True)

class ChangesetCorpus(gensim.corpora.TextCorpus):
    """ Iterates over all files within `top_dir`, yielding each file as
    a document and the fully qualified name of the file as the metadata.

    """

    def __init__(self, git_dir):
        super(ChangesetCorpus, self).__init__(git_dir)

        self.repo = dulwich.repo.Repo(git_dir)

    def get_texts(self):
        self.length = 0
        if self.metadata:
            yield [''], ('', '')
        else:
            yield ['']

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

if __name__ == '__main__':
    import nose
    nose.main()

from nose.tools import *
import unittest

import os.path
module_path = os.path.dirname(__file__) # needed because sample data files are located in the same folder
datapath = lambda fname: os.path.join(module_path, u'test_data', fname)

from io import StringIO
from src import generation


class TestGeneration(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_docs(self):
        fname = u'butts.txt'
        expected = u'butts.txt en burgers cats dogs hotdogs\n'
        with StringIO(u'burgers\ncats\ndogs hotdogs\n') as i:
            with StringIO() as o:
                generation.generate_docs(fname, i, o)
                result = o.getvalue()

        self.assertEqual(result, expected)

        i = "burgers\ncats\ndogs hotdogs\n".splitlines()
        with StringIO() as o:
            generation.generate_docs(fname, i, o)
            result = o.getvalue()

        self.assertEqual(result, expected)

    def test_multitext_corpus(self):
        basepath = datapath(u'multitext/')
        corpus = generation.MultiTextCorpus(basepath)
        corpus.metadata = True
        docs = list(corpus)
        self.assertEqual(len(corpus), 11) # check the corpus builds correctly
        self.assertEqual(len(docs), 11) # the deerwester corpus always has nine documents, no matter what format

        documents = [
                ([u'human', u'machine', u'interface', u'for', u'lab', u'abc', u'computer', u'applications'], 
                    (basepath + 'a/0.txt',)),
                ([u'a', u'survey', u'of', u'user', u'opinion', u'of', u'computer', u'system', u'response', u'time'],
                    (basepath + 'a/1.txt',)),
                ([u'the', u'eps', u'user', u'interface', u'management', u'system'],
                    (basepath + 'b/2.txt',)),
                ([u'system', u'and', u'human', u'system', u'engineering', u'testing', u'of', u'eps'],
                    (basepath + 'b/3.txt',)),
                ([u'relation', u'of', u'user', u'perceived', u'response', u'time', u'to', u'error', u'measurement'],
                    (basepath + 'c/4.txt',)),
                ([u'the', u'generation', u'of', u'random', u'binary', u'unordered', u'trees'],
                    (basepath + 'c/e/5.txt',)),
                ([u'the', u'intersection', u'graph', u'of', u'paths', u'in', u'trees'],
                    (basepath + 'c/f/6.txt',)),
                ([u'graph', u'minors', u'iv', u'widths', u'of', u'trees', u'and', u'well', u'quasi', u'ordering'],
                    (basepath + '7.txt',)),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'dos.txt',)),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'mac.txt',)),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'unix.txt',)),
                ]

        for docmeta in corpus.get_texts():
            doc, meta = docmeta
            doc = list(doc)
            docmeta = doc, meta
            self.assertIn(docmeta, documents)


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
        if not os.path.exists(datapath('multitext_git')):
            extraction_path = datapath('')
            gz = datapath('multitext_git.tar.gz')

            import tarfile
            with tarfile.open(gz) as tar:
                tar.extractall(extraction_path)

    def test_multitext_metadata_get_texts(self):
        basepath = datapath(u'multitext/')
        corpus = generation.MultiTextCorpus(basepath)
        corpus.metadata = True
        docs = list(corpus)
        self.assertEqual(len(corpus), 11) # check the corpus builds correctly
        self.assertEqual(len(docs), 11)

        documents = [
                ([u'human', u'machine', u'interface', u'for', u'lab', u'abc', u'computer', u'applications'],
                    (basepath + 'a/0.txt', u'en')),
                ([u'a', u'survey', u'of', u'user', u'opinion', u'of', u'computer', u'system', u'response', u'time'],
                    (basepath + 'a/1.txt', u'en')),
                ([u'the', u'eps', u'user', u'interface', u'management', u'system'],
                    (basepath + 'b/2.txt', u'en')),
                ([u'system', u'and', u'human', u'system', u'engineering', u'testing', u'of', u'eps'],
                    (basepath + 'b/3.txt', u'en')),
                ([u'relation', u'of', u'user', u'perceived', u'response', u'time', u'to', u'error', u'measurement'],
                    (basepath + 'c/4.txt', u'en')),
                ([u'the', u'generation', u'of', u'random', u'binary', u'unordered', u'trees'],
                    (basepath + 'c/e/5.txt', u'en')),
                ([u'the', u'intersection', u'graph', u'of', u'paths', u'in', u'trees'],
                    (basepath + 'c/f/6.txt', u'en')),
                ([u'graph', u'minors', u'iv', u'widths', u'of', u'trees', u'and', u'well', u'quasi', u'ordering'],
                    (basepath + '7.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'dos.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'mac.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (basepath + 'unix.txt', u'en')),
                ]

        for docmeta in corpus.get_texts():
            doc, meta = docmeta
            doc = list(doc) # generators, woo?
            docmeta = doc, meta # get a non (generator, metadata) pair
            self.assertIn(docmeta, documents)

    def test_multitext_get_texts(self):
        basepath = datapath(u'multitext/')
        corpus = generation.MultiTextCorpus(basepath)
        docs = list(corpus)
        self.assertEqual(len(corpus), 11) # check the corpus builds correctly
        self.assertEqual(len(docs), 11)

        documents = [
                [u'human', u'machine', u'interface', u'for', u'lab', u'abc', u'computer', u'applications'],
                [u'a', u'survey', u'of', u'user', u'opinion', u'of', u'computer', u'system', u'response', u'time'],
                [u'the', u'eps', u'user', u'interface', u'management', u'system'],
                [u'system', u'and', u'human', u'system', u'engineering', u'testing', u'of', u'eps'],
                [u'relation', u'of', u'user', u'perceived', u'response', u'time', u'to', u'error', u'measurement'],
                [u'the', u'generation', u'of', u'random', u'binary', u'unordered', u'trees'],
                [u'the', u'intersection', u'graph', u'of', u'paths', u'in', u'trees'],
                [u'graph', u'minors', u'iv', u'widths', u'of', u'trees', u'and', u'well', u'quasi', u'ordering'],
                [u'graph', u'minors', u'a', u'survey'],
                [u'graph', u'minors', u'a', u'survey'],
                [u'graph', u'minors', u'a', u'survey'],
                ]

        for doc in corpus.get_texts():
            doc = list(doc) # generators, woo?
            self.assertIn(doc, documents)

    def test_multitext_docs(self):
        basepath = datapath(u'multitext/')
        corpus = generation.MultiTextCorpus(basepath)
        docs = list(corpus)
        self.assertEqual(len(corpus), 11) # check the corpus builds correctly
        self.assertEqual(len(docs), 11)

        documents = [
                [(u'human', 1),
                    (u'machine', 1),
                    (u'interface', 1),
                    (u'for', 1),
                    (u'lab', 1),
                    (u'abc', 1),
                    (u'computer', 1),
                    (u'applications', 1)],

                [(u'a', 1),
                    (u'survey', 1),
                    (u'of', 2),
                    (u'user', 1),
                    (u'opinion', 1),
                    (u'computer', 1),
                    (u'system', 1),
                    (u'response', 1),
                    (u'time', 1)],

                [(u'the', 1),
                    (u'eps', 1),
                    (u'user', 1),
                    (u'interface', 1),
                    (u'management', 1),
                    (u'system', 1)],

                [(u'system', 2),
                    (u'and', 1),
                    (u'human', 1),
                    (u'engineering', 1),
                    (u'testing', 1),
                    (u'of', 1),
                    (u'eps', 1)],

                [(u'relation', 1),
                    (u'of', 1),
                    (u'user', 1),
                    (u'perceived', 1),
                    (u'response', 1),
                    (u'time', 1),
                    (u'to', 1),
                    (u'error', 1),
                    (u'measurement', 1)],

                [(u'the', 1),
                    (u'generation', 1),
                    (u'of', 1),
                    (u'random', 1),
                    (u'binary', 1),
                    (u'unordered', 1),
                    (u'trees', 1)],

                [(u'the', 1),
                        (u'intersection', 1),
                        (u'graph', 1),
                        (u'of', 1),
                        (u'paths', 1),
                        (u'in', 1),
                        (u'trees', 1)],

                [(u'graph', 1),
                        (u'minors', 1),
                        (u'iv', 1),
                        (u'widths', 1),
                        (u'of', 1),
                        (u'trees', 1),
                        (u'and', 1),
                        (u'well', 1),
                        (u'quasi', 1),
                        (u'ordering', 1)],

                [(u'graph', 1),
                        (u'minors', 1),
                        (u'a', 1),
                        (u'survey', 1)],
                ]

        documents = [set(x) for x in documents]


        # terrible test, need to calculate each doc like other two tests
        for doc in corpus:
            self.assertGreater(len(doc), 0)

            # convert the document to text freq since we don't know the
            # term ids ahead of time for testing.
            textdoc = set((unicode(corpus.dictionary[x[0]]), x[1]) for x in doc)
            self.assertIn(textdoc, documents)

    def test_git_test_extraction(self):
        assert os.path.exists(datapath('multitext_git'))



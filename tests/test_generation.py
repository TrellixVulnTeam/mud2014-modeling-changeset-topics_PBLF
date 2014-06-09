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

import unittest
import os.path
from io import StringIO

from nose.tools import *

from src import generation

# datapath is now a useful function for building paths to test files
module_path = os.path.dirname(__file__)
datapath = lambda fname: os.path.join(module_path, u'test_data', fname)

class TestMultitextCorpus(unittest.TestCase):
    def setUp(self):
        self.basepath = datapath(u'multitext/')
        self.corpus = generation.MultiTextCorpus(self.basepath)
        self.docs = list(self.corpus)

    def test_length(self):
        self.assertEqual(len(self.corpus), 11)
        self.assertEqual(len(self.docs), 11)

    def test_metadata_get_texts(self):
        self.corpus.metadata = True

        documents = [
                ([u'human', u'machine', u'interface', u'for', u'lab', u'abc', u'computer', u'applications'],
                    (self.basepath + 'a/0.txt', u'en')),
                ([u'a', u'survey', u'of', u'user', u'opinion', u'of', u'computer', u'system', u'response', u'time'],
                    (self.basepath + 'a/1.txt', u'en')),
                ([u'the', u'eps', u'user', u'interface', u'management', u'system'],
                    (self.basepath + 'b/2.txt', u'en')),
                ([u'system', u'and', u'human', u'system', u'engineering', u'testing', u'of', u'eps'],
                    (self.basepath + 'b/3.txt', u'en')),
                ([u'relation', u'of', u'user', u'perceived', u'response', u'time', u'to', u'error', u'measurement'],
                    (self.basepath + 'c/4.txt', u'en')),
                ([u'the', u'generation', u'of', u'random', u'binary', u'unordered', u'trees'],
                    (self.basepath + 'c/e/5.txt', u'en')),
                ([u'the', u'intersection', u'graph', u'of', u'paths', u'in', u'trees'],
                    (self.basepath + 'c/f/6.txt', u'en')),
                ([u'graph', u'minors', u'iv', u'widths', u'of', u'trees', u'and', u'well', u'quasi', u'ordering'],
                    (self.basepath + '7.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (self.basepath + 'dos.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (self.basepath + 'mac.txt', u'en')),
                ([u'graph', u'minors', u'a', u'survey'],
                    (self.basepath + 'unix.txt', u'en')),
                ]

        for docmeta in self.corpus.get_texts():
            doc, meta = docmeta
            doc = list(doc) # generators, woo?
            docmeta = doc, meta # get a non (generator, metadata) pair
            self.assertIn(docmeta, documents)

    def test_get_texts(self):
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

        for doc in self.corpus.get_texts():
            doc = list(doc) # generators, woo?
            self.assertIn(doc, documents)

    def test_docs(self):
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
        for doc in self.corpus:
            self.assertGreater(len(doc), 0)

            # convert the document to text freq since we don't know the
            # term ids ahead of time for testing.
            textdoc = set((unicode(self.corpus.dictionary[x[0]]), x[1]) for x in doc)
            self.assertIn(textdoc, documents)


class TestChangesetCorpus(unittest.TestCase):
    def setUp(self):
        self.basepath = datapath(u'multitext_git/')
        if not os.path.exists(self.basepath):
            extraction_path = datapath('')
            gz = datapath(u'multitext_git.tar.gz')

            import tarfile
            with tarfile.open(gz) as tar:
                tar.extractall(extraction_path)

        self.corpus = generation.ChangesetCorpus(self.basepath)
        self.docs = list(self.corpus)

    def tset_corpus_lengths(self):
        self.assertEqual(len(self.corpus), 5) # check the corpus builds correctly
        self.assertEqual(len(self.docs), 5)

    def test_changeset_get_texts(self):
        pass

    def test_changeset_docs(self):
        pass

    def test_changeset_metadata_get_texts(self):
        pass


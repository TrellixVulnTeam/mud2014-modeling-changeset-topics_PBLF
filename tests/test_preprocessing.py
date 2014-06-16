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

from src.preprocessing import split, remove_stops

# datapath is now a useful function for building paths to test files
module_path = os.path.dirname(__file__)
datapath = lambda fname: os.path.join(module_path, u'test_data', fname)

class PreprocessTests(unittest.TestCase):
    def test_split(self):
        """ Basic splitting works """
        string = ["420yoloSwag_4evr-Ever", "batMan-and_Robin", "helloWorld---_"]
        splitted = split(string)
        #assert splitted != ["yolo", "Swag", "evr", "Ever", "bat", "Man", "and", "robin", "hello", "World"] , "test failed"
        expected = ["yolo", "Swag", "evr", "Ever", "bat", "Man", "and", "robin", "hello", "World"]
        self.assertEqual(list(splitted), expected)


    def test_split_hard(self):
        """Split tokens into terms using the following rules:

            0. All digits are discarded
            1. A sequence beginning with an lc letter must be followed by lc letters
            2. A sequence beginning with an uc letter can be followed by either:
                a. One or more uc letters
                b. One or more lc letters

        """
        cases = dict({
                'camelCase': ('camel', 'Case'),
                'CamelCase': ('Camel', 'Case'),
                'camel2case': ('camel', 'case'),
                'camel2Case': ('camel', 'Case'),
                'word': ('word'),
                'HTML': ('HTML'),
                'readXML': ('read', 'XML'),
                'XMLRead': ('XML', 'Read'),
                'firstMIDDLELast': ('first', 'MIDDLE', 'Last'),
                'CFile': ('C', 'File'),
                'Word2Word34': ('Word', 'Word'),
                'WORD123Word': ('WORD', 'Word'),
                'c_amelCase': ('c', 'amel', 'Case'),
                'CamelC_ase': ('Camel', 'C', 'ase'),
                'camel2_case': ('camel', 'case'),
                'camel_2Case': ('camel', 'Case'),
                'word': ('word'),
                'HTML': ('HTML'),
                'read_XML': ('read', 'XML'),
                'XML_Read': ('XML', 'Read'),
                'firstM_IDDL_ELast': ('first', 'M', 'IDDL', 'E', 'Last'),
                'the_CFile': ('the', 'C', 'File'),
                'Word_2_Word3_4': ('Word', 'Word'),
                'WO_RD123W_or_d': ('WO', 'RD', 'W', 'or', 'd'),
                })
        for term, expected in cases.items():
            result = split(term)
            self.assertEqual(tuple(result), expected)

    def test_split_creates_generator(self):
        """ Split tokens creates a generator """
        result = split('butts')
        self.assertIs(result, type(x for x in xrange(1)))


    def test_stops(self): 
        input = ['test', 'the']
        expected = ['test']
        stops = ['the']
        result = remove_stops(input, stops)
        self.assertEqual(list(result), expected)

    def test_stops_creates_generator(self):
        """ Remove stops creates a generator """
        input = ['test', 'the']
        expected = ['test']
        stops = ['the']
        result = remove_stops(input, stops)
        self.assertIs(result, type(x for x in xrange(1)))

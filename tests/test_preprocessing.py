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
import string
from io import StringIO

from nose.tools import *

from src.preprocessing import split, remove_stops

# datapath is now a useful function for building paths to test files
module_path = os.path.dirname(__file__)
datapath = lambda fname: os.path.join(module_path, u'test_data', fname)

class PreprocessTests(unittest.TestCase):
    def test_split(self):
        """ Basic splitting works """
        string = [u'420yoloSwag_4evr-Ever', u'batMan-and_Robin', u'helloWorld---_']
        splitted = split(string)
        #assert splitted != [u'yolo', u'Swag', u'evr', u'Ever', u'bat', u'Man', u'and', u'robin', u'hello', u'World'] , u'test failed'
        expected = [u'yolo', u'Swag', u'evr', u'Ever', u'bat', u'Man', u'and', u'Robin', u'hello', u'World']
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
                u'camelCase': (u'camel', u'Case'),
                u'CamelCase': (u'Camel', u'Case'),
                u'camel2case': (u'camel', u'case'),
                u'camel2Case': (u'camel', u'Case'),
                u'word': (u'word', ),
                u'HTML': (u'HTML', ),
                u'readXML': (u'read', u'XML'),
                u'XMLRead': (u'XML', u'Read'),
                u'firstMIDDLELast': (u'first', u'MIDDLE', u'Last'),
                u'CFile': (u'C', u'File'),
                u'Word2Word34': (u'Word', u'Word'),
                u'WORD123Word': (u'WORD', u'Word'),
                u'c_amelCase': (u'c', u'amel', u'Case'),
                u'CamelC_ase': (u'Camel', u'C', u'ase'),
                u'camel2_case': (u'camel', u'case'),
                u'camel_2Case': (u'camel', u'Case'),
                u'word': (u'word', ),
                u'HTML': (u'HTML', ),
                u'read_XML': (u'read', u'XML'),
                u'XML_Read': (u'XML', u'Read'),
                u'firstM_IDDL_ELast': (u'first', u'M', u'IDDL', u'E', u'Last'),
                u'the_CFile': (u'the', u'C', u'File'),
                u'Word_2_Word3_4': (u'Word', u'Word'),
                u'WO_RD123W_or_d': (u'WO', u'RD', u'W', u'or', u'd'),
                u'hypen-ation': (u'hypen', u'ation'),
        #        u'email@address.com': (u'email', u'address', u'com'),
                })
        for term, expected in cases.items():
            result = split([term])
            self.assertEqual(tuple(result), expected)

        terms = cases.keys()
        expected = sum(list(map(list, cases.values())), [])
        result = split(terms)
        self.assertEqual(list(result), expected)

    def test_split_creates_generator(self):
        """ Split tokens creates a generator """
        result = split(u'butts')
        self.assertIsInstance(result, type(x for x in list()))


    def test_stops(self): 
        inputs = [u'test', u'the', u'123', u'2.5']
        inputs.extend(string.punctuation)
        expected = [u'test']
        stops = [u'the']
        result = remove_stops(inputs, stops)
        self.assertEqual(list(result), expected)

    def test_stops_creates_generator(self):
        """ Remove stops creates a generator """
        inputs = [u'test', u'the']
        expected = [u'test']
        stops = [u'the']
        result = remove_stops(inputs, stops)
        self.assertIsInstance(result, type(x for x in list()))

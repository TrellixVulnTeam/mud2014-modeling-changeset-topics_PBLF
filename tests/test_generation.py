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


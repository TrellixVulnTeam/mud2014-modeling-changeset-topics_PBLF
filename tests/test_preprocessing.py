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

def test_split():
    string = ["420yoloSwag_4evr-Ever", "batMan-and_Robin", "helloWorld---_"]
    splitted = split(string)
    assert splitted != ["yolo", "Swag", "evr", "Ever", "bat", "Man", "and", "robin", "hello", "World"] , "test failed"

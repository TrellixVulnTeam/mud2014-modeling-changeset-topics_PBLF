#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Topic of Change',
    version='0.0.1',
    description='',
    long_description=readme,
    author='Christopher S. Corley',
    author_email='cscorley@crimson.ua.edu',
    url='https://github.com/cscorley/topic-of-change',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    keywords = [],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        ],
    py_module=['topicofchange'],
    install_requires=['Click',
        ],
    entry_points='''
        [console_scripts]
        topicofchange=src:cli:cli
    '''
)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function

import csv
import sys
from collections import namedtuple

import click
import gittle
import dulwich
from gensim.corpora import MalletCorpus
from gensim.models import LdaModel

import utils
from corpora import MultiTextCorpus, ChangesetCorpus


class Config:
    def __init__(self):
        self.verbose = False
        self.path = './'
        self.project = None
        self.repo = None
        self.file_corpus = None
        self.changeset_corpus = None
        self.num_topics = 100
        self.alpha = 'auto' # or can set a float
        # set all possible config options here

def error(msg, errorno=1):
    print(msg, file=sys.stderr)
    sys.exit(errorno)


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--path', default='/var/opt/topic-of-change/',
        help="Set the directory to work within")
@click.argument('project')
@pass_config
def main(config, verbose, path, project):
    """
    Topic of Change
    """

    # Only set config items here, this function is unused otherwise.
    config.verbose = verbose
    config.path = path
    with open("projects.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        Project = namedtuple('Project',  ' '.join(header))

        # figure out which column index contains the project name
        name_idx = header.index("name")

        # find the project in the csv, adding it's info to config
        for row in reader:
            if project == row[name_idx]:
                # 🎶  do you believe in magicccccc
                # in a young girl's heart? 🎶
                config.project = Project(*row)
                break

        # we can access project info by:
        #    config.project.url => "http://..."
        #    config.project.name => "Blah Name"

        if config.project is None:
            error("Could not find the project '%s' in 'projects.csv'!" % project)


@main.command()
@pass_config
@click.pass_context
def clone(context, config):
    """
    Clones the project repository
    """
    print('Cloning repo for: %s' % config.project.name)

    tries = 10
    while config.repo is None and tries > 0:
        tries -= 1
        try:
            config.repo = open_or_clone(config.path, config.project)
        except dulwich.errors.GitProtocolError as e:
            config.repo = None

    if config.repo is None:
        error('Could not clone repository within 10 tries :(')

def open_or_clone(path, project):
    full_path = path + project.name
    try:
        return gittle.Gittle(full_path).repo
    except dulwich.errors.NotGitRepository:
        return gittle.Gittle.clone_bare(project.url, full_path).repo


@main.command()
@pass_config
@click.pass_context
def corpora(context, config):
    """
    Builds the basic corpora for a project
    """

    if config.repo is None:
        try:
            config.repo = gittle.Gittle(config.path + config.project.name).repo
        except dulwich.errors.NotGitRepository:
            error('Repository not cloned yet!')

    print('Creating corpora for: %s' % config.project.name)

    # build file-based corpus
    # try opening an previously made corpus first
    file_fname = config.path + config.project.name + '_files.mallet'
    try:
        file_corpus = MalletCorpus(file_fname)
        print('Opened previously created corpus at file %s' % file_fname)
    # build one if it doesnt exist
    except:
        print('Creating file-based corpus out of source files for '
            'release %s at commit %s' % (
                config.project.release, config.project.commit))

        file_corpus = MultiTextCorpus(config.repo, config.project.commit, lazy_dict=True)
        file_corpus.metadata = True
        MalletCorpus.serialize(file_fname, file_corpus,
                id2word=file_corpus.dictionary, metadata=True)

    # build changeset-based corpus
    changeset_fname = config.path + config.project.name + '_changesets.mallet'
    # try opening an previously made corpus first
    try:
        changeset_corpus = MalletCorpus(changeset_fname)
        print('Opened previously created corpus at file %s' % file_fname)
    # build one if it doesnt exist
    except:
        print('Creating changeset-based corpus out of source files for '
            'release %s for all commits reachable from %s' % (
                config.project.release, config.project.commit))

        changeset_corpus = ChangesetCorpus(config.repo, config.project.commit, lazy_dict=True)
        changeset_corpus.metadata = True
        MalletCorpus.serialize(changeset_fname, changeset_corpus,
                id2word=changeset_corpus.dictionary, metadata=True)

    config.file_corpus = file_corpus
    config.changeset_corpus = changeset_corpus


@main.command()
@pass_config
@click.pass_context
def model(context, config):
    """
    Builds a model for the corpora
    """
    print('Building topic models for: %s' % config.project.name)

    file_fname = config.path + config.project.name + '_files.lda'
    try:
        file_model = LdaModel.load(file_fname)
        print('Opened previously created model at file %s' % file_fname)
    except:
        if config.file_corpus is None:
            error('Corpora for building file models not found!')

        # TODO
        # Maybe look into various settings for num_topics?
        file_model = LdaModel(config.file_corpus,
                alpha=config.alpha,
                num_topics=config.num_topics)

        file_model.save(file_fname)

    config.file_model = file_model

    changeset_fname = config.path + config.project.name + '_changesets.lda'
    try:
        changeset_model = LdaModel.load(changeset_fname)
        print('Opened previously created model at changeset %s' % changeset_fname)
    except:
        if config.changeset_corpus is None:
            error('Corpora for building changeset models not found!')

        changeset_model = LdaModel(config.changeset_corpus,
                alpha=config.alpha,
                num_topics=config.num_topics)

        changeset_model.save(changeset_fname)

    config.changeset_model = changeset_model

@main.command()
@pass_config
@click.pass_context
def evaluate(context, config):
    """
    Evalutates the models
    """
    if config.file_model is None or config.changeset_model is None:
        error('Cannot evalutate LDA models not built yet!')

    print('Evalutating models for: %s' % config.project.name)

    print("File model KL:",
            score(config.file_model, utils.kullback_leibler_divergence))
    print("Changeset model KL:",
            score(config.changeset_model, utils.kullback_leibler_divergence))

def score(model, fn):
    total = 0
    for a, topic_a in norm_phi(model):
        score = 0
        for b, topic_b in norm_phi(model):
            if a == b:
                continue
            score += fn(topic_a, topic_b)
        print(a, score)
        total += score
    return total

def norm_phi(model):
    for topicid in range(model.num_topics):
        topic = model.state.get_lambda()[topicid]
        topic = topic / topic.sum() # normalize to probability dist
        yield topicid, topic


@main.command()
@pass_config
@click.pass_context
def run_all(context, config):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    print('Doing everything for: %s' % config.project.name)
    context.forward(clone)
    context.forward(corpora)
    context.forward(model)
    context.forward(evaluate)

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
import dulwich
import dulwich.repo
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
        self.file_model = None
        self.changeset_model = None
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
def corpora(context, config):
    """
    Builds the basic corpora for a project
    """

    git_path = config.path + config.project.name
    # open the repo
    try:
        config.repo = dulwich.repo.Repo(git_path)
    except dulwich.errors.NotGitRepository:
        error('Repository not cloned yet! Clone command: '
                'git clone %s %s' % (config.project.url, git_path))

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
            fname = config.path + config.project.name + '_files.mallet'
            try:
                config.file_corpus = MalletCorpus(fname)
                print('Opened previously created corpus at file %s' % fname)
            # build one if it doesnt exist
            except:
                error('Corpora for building file models not found!')


        # TODO
        # Maybe look into various settings for num_topics?
        file_model = LdaModel(config.file_corpus,
                id2word=config.file_corpus.id2word,
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
            fname = config.path + config.project.name + '_changesets.mallet'
            try:
                config.changeset_corpus = MalletCorpus(fname)
                print('Opened previously created corpus at file %s' % fname)
            # build one if it doesnt exist
            except:
                error('Corpora for building changeset models not found!')

        changeset_model = LdaModel(config.changeset_corpus,
                id2word=config.changeset_corpus.id2word,
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
    file_model = config.file_model
    changeset_model = config.changeset_model

    if file_model is None or changeset_model is None:
        file_fname = config.path + config.project.name + '_files.lda'
        try:
            file_model = LdaModel.load(file_fname)
            print('Opened previously created model at file %s' % file_fname)
        except:
            error('Cannot evalutate LDA models not built yet!')

        changeset_fname = config.path + config.project.name + '_changesets.lda'
        try:
            changeset_model = LdaModel.load(changeset_fname)
            print('Opened previously created model at changeset %s' % changeset_fname)
        except:
            error('Cannot evalutate LDA models not built yet!')

    print('Evalutating models for: %s' % config.project.name)

    file_scores = score(file_model, utils.kullback_leibler_divergence)
    changeset_scores = score(changeset_model, utils.kullback_leibler_divergence)

    file_total = sum(file_scores, key=lambda x: x[1])
    changeset_total = sum(changeset_scores, key=lambda x: x[1])

    print("File model KL:", file_total)
    print("Changeset model KL:", changeset_total)
    print("File model KL mean:", file_total / len(file_scores))
    print("Changeset model KL mean:", changeset_total / len(changeset_scores))

def score(model, fn):
    # thomas et al 2011 msr
    #
    scores = list()
    for a, topic_a in norm_phi(model):
        score = 0.0
        for b, topic_b in norm_phi(model):
            if a == b:
                continue
            score += fn(topic_a, topic_b)
        score *= (1.0 / (model.num_topics - 1))
        print(a, score)
        scores.append((a, score))
    return scores

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
    context.forward(corpora)
    context.forward(model)
    context.forward(evaluate)

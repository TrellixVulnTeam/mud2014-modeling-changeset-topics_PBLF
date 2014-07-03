#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

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


import logging

logger = logging.getLogger('mct')

class Config:
    def __init__(self):
        self.path = './'
        self.project = None
        self.repo = None
        self.file_corpus = None
        self.changeset_corpus = None
        self.file_model = None
        self.changeset_model = None
        self.fname_prefix = ''
        self.num_topics = 100
        self.alpha = 'symmetric' # or can set a float
        # set all possible config options here

def error(msg, errorno=1):
    logger.error(msg)
    sys.exit(errorno)


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--path', default='data/',
        help="Set the directory to work within")
@click.argument('project')
@pass_config
def main(config, verbose, path, project):
    """
    Modeling Changeset Topics
    """

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(name)s : %(funcName)s : %(message)s')

    if verbose:
        logging.root.setLevel(level=logging.DEBUG)
    else:
        logging.root.setLevel(level=logging.INFO)

    # Only set config items here, this function is unused otherwise.
    config.path = path
    if not config.path.endswith('/'):
        config.path += '/'

    utils.mkdir(config.path)

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

    config.fname_prefix = (config.path +
                            config.project.name +
                            '-' +
                            config.project.commit[:8] + '-'
                            )


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

    logger.info('Creating corpora for: %s' % config.project.name)

    # build file-based corpus
    # try opening an previously made corpus first
    file_fname = config.fname_prefix + 'file.mallet'
    try:
        file_corpus = MalletCorpus(file_fname)
        logger.info('Opened previously created corpus at file %s' % file_fname)
    # build one if it doesnt exist
    except:
        logger.info('Creating file-based corpus out of source files for '
            'release %s at commit %s' % (
                config.project.release, config.project.commit))

        file_corpus = MultiTextCorpus(config.repo, config.project.commit, lazy_dict=True)
        file_corpus.metadata = True
        MalletCorpus.serialize(file_fname, file_corpus,
                id2word=file_corpus.id2word, metadata=True)
        file_corpus.metadata = False
        file_corpus = MalletCorpus(file_fname)

    # build changeset-based corpus
    changeset_fname = config.fname_prefix + 'changeset.mallet'
    # try opening an previously made corpus first
    try:
        changeset_corpus = MalletCorpus(changeset_fname)
        logger.info('Opened previously created corpus at file %s' % changeset_fname)
    # build one if it doesnt exist
    except:
        logger.info('Creating changeset-based corpus out of source files for '
            'release %s for all commits reachable from %s' % (
                config.project.release, config.project.commit))

        changeset_corpus = ChangesetCorpus(config.repo, config.project.commit, lazy_dict=True)
        changeset_corpus.metadata = True
        MalletCorpus.serialize(changeset_fname, changeset_corpus,
                id2word=changeset_corpus.id2word, metadata=True)
        changeset_corpus.metadata = False
        changeset_corpus = MalletCorpus(changeset_fname)

    config.file_corpus = file_corpus
    config.changeset_corpus = changeset_corpus

@main.command()
@pass_config
@click.pass_context
def model(context, config):
    """
    Builds a model for the corpora
    """
    logger.info('Building topic models for: %s' % config.project.name)


    file_fname = config.fname_prefix + 'file.lda'
    try:
        file_model = LdaModel.load(file_fname)
        logger.info('Opened previously created model at file %s' % file_fname)
    except:
        if config.file_corpus is None:
            logger.info(a, score)
            fname = config.fname_prefix + 'file.mallet'
            try:
                config.file_corpus = MalletCorpus(fname)
                logger.info('Opened previously created corpus at file %s' % fname)
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

    changeset_fname = config.fname_prefix + 'changeset.lda'
    try:
        changeset_model = LdaModel.load(changeset_fname)
        logger.info('Opened previously created model at changeset %s' % changeset_fname)
    except:
        if config.changeset_corpus is None:
            fname = config.fname_prefix + 'changeset.mallet'
            try:
                config.changeset_corpus = MalletCorpus(fname)
                logger.info('Opened previously created corpus at file %s' % fname)
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
        file_fname = config.fname_prefix + 'file.lda'
        try:
            file_model = LdaModel.load(file_fname)
            logger.info('Opened previously created model at file %s' % file_fname)
        except:
            error('Cannot evalutate LDA models not built yet!')

        changeset_fname = config.fname_prefix + 'changeset.lda'
        try:
            changeset_model = LdaModel.load(changeset_fname)
            logger.info('Opened previously created model at changeset %s' % changeset_fname)
        except:
            error('Cannot evalutate LDA models not built yet!')

    logger.info('Evalutating models for: %s' % config.project.name)

    file_scores = utils.score(file_model, utils.kullback_leibler_divergence)
    changeset_scores = utils.score(changeset_model, utils.kullback_leibler_divergence)

    file_total = sum([x[1] for x in file_scores])
    changeset_total = sum([x[1] for x in changeset_scores])

    logger.info("File model KL: %f" % file_total)
    logger.info("Changeset model KL: %f" % changeset_total)
    logger.info("File model KL mean: %f" % (file_total / len(file_scores)))
    logger.info("Changeset model KL mean: %f" % (changeset_total / len(changeset_scores)))


@main.command()
@pass_config
@click.pass_context
def evaluate_corpora(context, config):
    file_fname = config.fname_prefix + 'file.mallet'
    try:
        file_corpus = MalletCorpus(file_fname)
    except:
        error('Corpora not built yet -- cannot evaluate')

    file_word_freq = list(reversed(sorted(count_words(file_corpus))))
    print("Top 10 words in files:", file_word_freq[:10])
    print("Bottom 10 words in files:", file_word_freq[-10:])

    changeset_fname = config.fname_prefix + 'changeset.mallet'
    try:
        changeset_corpus = MalletCorpus(changeset_fname)
    except:
        error('Corpora not built yet -- cannot evaluate')
    changeset_word_freq = list(reversed(sorted(count_words(changeset_corpus))))
    print("Top 10 words in changesets:", changeset_word_freq[:10])
    print("Bottom 10 words in changesets:", changeset_word_freq[-10:])

def count_words(corpus):
    word_freq = dict()
    for doc in corpus:
        for word, count in doc:
            if word not in word_freq:
                word_freq[word] = 0

            word_freq[word] += count

    for word_id, freq in word_freq.items():
        yield freq, corpus.id2word[word_id]



@main.command()
@pass_config
@click.pass_context
def run_all(context, config):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    logger.info('Doing everything for: %s' % config.project.name)
    context.forward(corpora)
    context.forward(model)
    context.forward(evaluate)

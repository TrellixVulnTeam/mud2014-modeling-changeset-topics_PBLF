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
import os.path
import random
from collections import namedtuple

import numpy
import click
import dulwich
import dulwich.repo
from gensim.corpora import MalletCorpus, Dictionary
from gensim.models import LdaModel

import utils
from corpora import MultiTextCorpus, ChangesetCorpus, CommitLogCorpus


import logging

logger = logging.getLogger('topicofchange')

class Config:
    def __init__(self):
        self.path = './'
        self.project = None
        self.repo = None
        self.corpus_fname = ''
        self.model_fname = ''
        self.passes = 10
        self.num_topics = 100
        self.alpha = 'symmetric' # or can set a float
        # set all possible config options here

def error(msg, errorno=1):
    logger.error(msg)
    sys.exit(errorno)


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--num-topics', default=100)
@click.option('--verbose', is_flag=True)
@click.option('--path', default='data/',
        help="Set the directory to work within")
@click.argument('project')
@pass_config
def main(config, verbose, path, project, num_topics):
    """
    Topic of Change
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

    config.corpus_fname = (config.path +
                    config.project.name + '-' +
                    config.project.commit[:8] + '-' +
                    '%s.mallet')

    config.model_fname = (config.path +
                    config.project.name + '-' +
                    config.project.commit[:8] + '-' +
                    str(config.passes) + 'passes-' +
                    str(config.alpha) + 'alpha-' +
                    str(config.num_topics) + 'topics-' +
                    '%s.lda')

    config.num_topics = num_topics

    git_path = config.path + config.project.name
    # open the repo
    try:
        config.repo = dulwich.repo.Repo(git_path)
    except dulwich.errors.NotGitRepository:
        error('Repository not cloned yet! Clone command: '
                'git clone %s %s' % (config.project.url, git_path))


@main.command()
@pass_config
@click.pass_context
def corpora(context, config):
    """
    Builds the basic corpora for a project
    """

    logger.info('Creating corpora for: %s' % config.project.name)

    create_corpus(config, MultiTextCorpus)
    create_corpus(config, ChangesetCorpus)
    create_corpus(config, CommitLogCorpus)

@main.command()
@pass_config
@click.pass_context
def model(context, config):
    """
    Builds a model for the corpora
    """
    logger.info('Building topic models for: %s' % config.project.name)

    create_model(config, MultiTextCorpus)
    create_model(config, ChangesetCorpus)
    create_model(config, CommitLogCorpus)

@main.command()
@pass_config
@click.pass_context
def evaluate_distinctiveness(context, config):
    """
    Evalutates the models
    """
    logger.info('Evalutating distinctiveness of models for: %s' % config.project.name)

    create_evaluation_distinctiveness(config, MultiTextCorpus)
    create_evaluation_distinctiveness(config, ChangesetCorpus)
    create_evaluation_distinctiveness(config, CommitLogCorpus)

@main.command()
@pass_config
@click.pass_context
def evaluate_corpora(context, config):
    logger.info('Evaluating corpus for: %s' % config.project.name)

    create_evaluation_corpora(config, MultiTextCorpus)
    create_evaluation_corpora(config, ChangesetCorpus)
    create_evaluation_corpora(config, CommitLogCorpus)

@main.command()
@pass_config
@click.pass_context
def evaluate_perplexity(context, config):
    logger.info('Evalutating perplexity of models for: %s' % config.project.name)

    create_evaluation_perplexity(config, MultiTextCorpus)
    create_evaluation_perplexity(config, ChangesetCorpus)
    create_evaluation_perplexity(config, CommitLogCorpus)

@main.command()
@pass_config
@click.pass_context
def evaluate_log(context, config):
    logger.info('Evalutating models for: %s' % config.project.name)

    model_fname = config.model_fname % ChangesetCorpus.__name__
    changeset_fname = config.corpus_fname % ChangesetCorpus.__name__
    commit_fname = config.corpus_fname % CommitLogCorpus.__name__

    try:
        commit_id2word = Dictionary.load(commit_fname + '.dict')
        commit_corpus = MalletCorpus(commit_fname, id2word=commit_id2word)
        changeset_id2word = Dictionary.load(changeset_fname + '.dict')
        changeset_corpus = MalletCorpus(changeset_fname, id2word=changeset_id2word)
    except:
        error('Corpora not built yet -- cannot evaluate')

    try:
        model = LdaModel.load(model_fname)
        logger.info('Opened previously created model at file %s' % model_fname)
    except:
        error('Cannot evalutate LDA models not built yet!')


    changeset_doc_topic = get_doc_topic(changeset_corpus, model)
    commit_doc_topic = get_doc_topic(commit_corpus, model)

    assert commit_doc_topic.keys() == changeset_doc_topic.keys()

    first_shared = dict()
    for id_ in commit_doc_topic:
        assert len(commit_doc_topic[id_]) == len(changeset_doc_topic[id_])
        i = 0
        commit_topics = [topic[0] for topic in commit_doc_topic[id_]]
        changeset_topics = [topic[0] for topic in changeset_doc_topic[id_]]

        maximum = max(len(commit_topics), len(changeset_topics))
        minimum = maximum

        for i, topic in enumerate(commit_topics):
            if topic in changeset_topics:
                j = changeset_topics.find(topic)
                minimum = min(minimum, max(i, j))

        for i, topic in enumerate(changeset_topics):
            if topic in changeset_topics:
                j = commit_topics.find(topic)
                minimum = min(minimum, max(i, j))

        first_shared[id_] = minimum

        if minimum == maximum:
            logger.info('No common topics found for %s' % id_)
            first_shared[id_] = None

    mean = sum(first_shared.values()) / len(first_shared)

    with open('evaluate-log-results.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow([model_fname, mean] + list(first_shared.values()))

def get_doc_topic(corpus, model):
    doc_topic = dict()
    corpus.metadata = True
    for doc, id_ in corpus:
        doc_topic[id_] = model[doc]

    corpus.metadata = False
    return list(reversed(sorted(doc_topic, key=lambda x: x[1])))

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
    context.forward(evaluate_distinctiveness)
    context.forward(evaluate_corpora)
    context.forward(evaluate_perplexity)
    context.forward(evaluate_log)


def create_corpus(config, Kind):
    model_fname = config.model_fname % Kind.__name__
    corpus_fname = config.corpus_fname % Kind.__name__

    if not os.path.exists(corpus_fname):
        corpus = Kind(config.repo, config.project.commit, lazy_dict=True)
        corpus.metadata = True
        MalletCorpus.serialize(corpus_fname, corpus, id2word=corpus.id2word, metadata=True)
        corpus.metadata = False
        corpus.id2word.save(corpus_fname + '.dict')

def create_model(config, Kind):
    model_fname = config.model_fname % Kind.__name__
    corpus_fname = config.corpus_fname % Kind.__name__

    if not os.path.exists(model_fname):
        try:
            id2word = Dictionary.load(corpus_fname + '.dict')
            corpus = MalletCorpus(corpus_fname, id2word=id2word)
            logger.info('Opened previously created corpus at file %s' % corpus_fname)
        except:
            error('Corpora for building file models not found!')

        file_model = LdaModel(corpus,
                id2word=corpus.id2word,
                alpha=config.alpha,
                passes=config.passes,
                num_topics=config.num_topics)

        file_model.save(model_fname)

def create_evaluation_distinctiveness(config, Kind):
    model_fname = config.model_fname % Kind.__name__
    corpus_fname = config.corpus_fname % Kind.__name__

    try:
        model = LdaModel.load(model_fname)
        logger.info('Opened previously created model at file %s' % model_fname)
    except:
        error('Cannot evalutate LDA models not built yet!')

    scores = utils.score(model, utils.kullback_leibler_divergence)
    total = sum([x[1] for x in scores])

    logger.info("%s model KL: %f" % (model_fname, total))
    with open(config.path + 'evaluate-results.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow([model_fname, total])

    etas = list()
    for topic in model.state.get_lambda():
        topic_eta = list()
        for p_w in topic:
            topic_eta.append(p_w * numpy.log2(p_w))
        etas.append(-sum(topic_eta))

    entropy = sum(etas) / len(etas)

    logger.info("%s model entropy mean: %f" % (model_fname, entropy))
    with open(config.path + 'evaluate-entropy-results.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow([model_fname, entropy])


def create_evaluation_corpora(config, Kind):
    corpus_fname = config.corpus_fname % Kind.__name__

    try:
        id2word = Dictionary.load(corpus_fname + '.dict')
        corpus = MalletCorpus(corpus_fname, id2word=id2word)
    except:
        error('Corpora not built yet -- cannot evaluate')

    word_freq = list(reversed(sorted(count_words(corpus))))
    print("Top 10 words in %s: %s", (corpus_fname, str(word_freq[:10])))
    print("Bottom 10 words in %s: %s", (corpus_fname, str(word_freq[-10:])))

def count_words(corpus):
    word_freq = dict()
    for doc in corpus:
        for word, count in doc:
            if word not in word_freq:
                word_freq[word] = 0

            word_freq[word] += count

    for word_id, freq in word_freq.items():
        yield freq, corpus.id2word[word_id]

def create_evaluation_perplexity(config, Kind):
    model_fname = config.model_fname % Kind.__name__
    corpus_fname = config.corpus_fname % Kind.__name__

    try:
        id2word = Dictionary.load(corpus_fname + '.dict')
        corpus = MalletCorpus(corpus_fname, id2word=id2word)
    except:
        error('Corpora not built yet -- cannot evaluate')

    pwb = perplexity(corpus)
    with open(config.path + 'evaluate-perplexity-results.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow([model_fname, pwb])

def perplexity(corpus):
    held_out = list()
    training = list()
    target_len = int(0.1 * len(corpus))
    logger.info('Calculating perplexity with held-out %d of %d documents' % (target_len, len(corpus)))

    ids = set()
    while len(ids) < target_len:
        ids.add(random.randint(0, len(corpus)))

    for doc_id, doc in enumerate(corpus):
        if doc_id in ids:
            held_out.append(doc)
        else:
            training.append(doc)

    model = LdaModel(training,
            id2word=corpus.id2word,
            alpha=config.alpha,
            passes=config.passes,
            num_topics=config.num_topics)

    return model.log_perplexity(held_out)


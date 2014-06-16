from __future__ import print_function

import click

class Config:
    def __init__(self):
        self.verbose = False
        self.base_path = '.'
        self.project = None
        # set all possible config options here


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--base_path', default='/var/opt/topic-of-change/',
        help="Set the directory to work within")
@click.argument('project')
@pass_config
def cli(config, verbose, base_path, project):
    """
    Modeling Changeset Topics
    """
    # Only set config items here, this function is unused otherwise.
    config.verbose = verbose
    config.base_path = base_path
    config.project = project


@cli.command()
@pass_config
def clone(config):
    """
    Clones the project repository
    """
    if config.verbose:
        print('We are in verbose mode.')

    print('Cloning repo for: %s' % config.project)

@cli.command()
#@click.option('--repeat', default=1,
#        help='How many times to greet the thing.')
@click.argument('project')
@pass_config
def corpora(config):
    """
    Builds the basic corpora for a project
    """
    if config.verbose:
        print('We are in verbose mode.')

    print('Creating corpus for: %s' % config.project)


@cli.command()
@pass_config
def preprocess(config):
    """
    Runs the preprocessing steps on a corpus
    """
    print('Preproccessing corpus for: %s' % config.project)


@cli.command()
@pass_config
def model(config):
    """
    Builds a model for the corpora
    """
    print('Building topic models for: %s' % config.project)


@cli.command()
@pass_config
def evaluate(config):
    """
    Evalutates the models
    """
    print('Evalutating models for: %s' % config.project)


@cli.command()
@pass_config
@click.pass_context
def run_all(context, config):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    print('Doing everything for: %s' % config.project)
    context.forward(clone)
    context.forward(corpora)
    context.forward(preprocess)
    context.forward(model)
    context.forward(evaluate)


from __future__ import print_function
import click
import csv
import sys

class Config:
    def __init__(self):
        self.verbose = False
        self.base_path = '.'
        self.project = {}
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
    Topic of Change
    """

    # Only set config items here, this function is unused otherwise.
    config.verbose = verbose
    config.base_path = base_path
    with open("projects.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        # figure out which column index contains the project name
        name_idx = header.index("short_name")

        found = False
        # find the project in the csv, adding it's info to config
        for row in reader:
            if project == row[name_idx]:
                for i, column in enumerate(header):
                    # now config.project["url"] => "http://[...]"
                    config.project[column] = row[i]
                found = True
                break

        if not found:
            print("Could not find the project '%s' in 'projects.csv'!" % project, file=sys.stderr)
            sys.exit(1)

@cli.command()
@pass_config
def clone(config):
    """
    Clones the project repository
    """
    if config.verbose:
        print('We are in verbose mode.')

    print('Cloning repo for: %s' % config.project["name"])

@cli.command()
@pass_config
def corpora(config):
    """
    Builds the basic corpora for a project
    """
    if config.verbose:
        print('We are in verbose mode.')

    print('Creating corpus for: %s' % config.project["name"])


@cli.command()
@pass_config
def preprocess(config):
    """
    Runs the preprocessing steps on a corpus
    """
    print('Preproccessing corpus for: %s' % config.project["name"])


@cli.command()
@pass_config
def model(config):
    """
    Builds a model for the corpora
    """
    print('Building topic models for: %s' % config.project["name"])


@cli.command()
@pass_config
def evaluate(config):
    """
    Evalutates the models
    """
    print('Evalutating models for: %s' % config.project["name"])


@cli.command()
@pass_config
@click.pass_context
def run_all(context, config):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    print('Doing everything for: %s' % config.project["name"])
    context.forward(clone)
    context.forward(corpora)
    context.forward(preprocess)
    context.forward(model)
    context.forward(evaluate)

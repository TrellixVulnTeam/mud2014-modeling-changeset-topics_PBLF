from __future__ import print_function

import click

class Config:
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    """ Click """
    config.verbose = verbose

@cli.command()
@click.option('--string', default='World',
        help='This is the thing that is greeted.')
@click.option('--repeat', default=1,
        help='How many times to greet the thing.')
@click.argument('out', type=click.File('w'), default='-',
        required=False)
@pass_config
def say(config, string, repeat, out):
    if config.verbose:
        print('We are in verbose mode.')
    for x in xrange(repeat):
        print('Hello, %s!' % string, file=out)

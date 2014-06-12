from __future__ import print_function

import click

@click.command()
@click.option('--string', default='World',
        help='This is the thing that is greeted.')
def cli(string):
    """ Click """
    print(string)

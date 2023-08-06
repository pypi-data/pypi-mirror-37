# -*- coding: utf-8 -*-
"""
uberping.cli - command line stuff
"""

import click
import subprocess

from .settings import Config

uberping_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--cache', is_flag=True,
              help='Enables caching mode.')
@uberping_config
def cli(config, verbose, cache):
    config.verbose = verbose
    config.cache = cache


@cli.command()
@click.option('--address', required=True, prompt='Destination address',
              help='Destination address to ping')
def ping(address):
    """Ping an ip address five times."""
    print(subprocess.check_output(['ping', '-c', '5', address]).decode())


def main():
    cli()

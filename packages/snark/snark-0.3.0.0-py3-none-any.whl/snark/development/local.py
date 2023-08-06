import click

import snark
from snark import config
from snark.log import configure_logger
from snark.main import add_commands


@click.group()
@click.option('-v', '--verbose', count=True, help='Devel debugging')
def cli(verbose):
    config.SNARK_REST_ENDPOINT = "http://127.0.0.1:5000"
    config.SNARK_HYPER_ENDPOINT = "http://127.0.0.1:8000"
    configure_logger(verbose)

add_commands(cli)

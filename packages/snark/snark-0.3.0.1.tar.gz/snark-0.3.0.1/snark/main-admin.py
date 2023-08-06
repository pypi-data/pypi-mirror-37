import click
import sys

from snark.cli.auth          import login, logout
from snark.cli.pod_control   import start, stop, ls, admin_stop, admin_ls_all
from snark.cli.data_transfer import push, pull
from snark.cli.connect       import attach
from snark.cli.hyper            import up, down, ps, logs
from snark import config
from snark.log import configure_logger

@click.group()
@click.option('-h', '--host', default='{}'.format(config.SNARK_REST_ENDPOINT), help='Snark server rest endpoint')
@click.option('-v', '--verbose', count=True, help='Devel debugging')
def cli(host, verbose):
    configure_logger(verbose)

def add_commands(cli):
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(start)
    cli.add_command(attach)
    cli.add_command(stop)
    cli.add_command(admin_stop)
    cli.add_command(admin_ls_all)
    cli.add_command(ls)
    cli.add_command(push)
    cli.add_command(pull)
    cli.add_command(up)
    cli.add_command(down)
    cli.add_command(ps)
    cli.add_command(logs)

add_commands(cli)

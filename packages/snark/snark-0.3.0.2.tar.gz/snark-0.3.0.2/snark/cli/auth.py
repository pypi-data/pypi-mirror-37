import click
from snark.log import logger
from snark import config
from snark.client.auth import AuthClient
from snark.token_manager import TokenManager


@click.command()
#@click.option('--token', is_flag=True, default=False,
#        help='Enter authentication tocken from {}'.format(config.GET_TOKEN_REST_SUFFIX))
@click.option('--username', '-u', default=None, help='Your Snark Ai username')
@click.option('--password', '-p', default=None, help='Your Snark AI password')
def login(username, password):
    """ Logs in to Snark AI"""
    token = ''
    if token:
        logger.info("Token login.")
        logger.degug("Getting the token...")
        token = click.prompt('Please paste the authentication token from {}'.format(config.GET_TOKEN_REST_SUFFIX,
            type=str, hide_input=True))
        token = token.strip()
        is_valid = AuthClient.check_token(token)
    else:
        logger.info("Please log in using Snark AI credentials. You can register at https://lab.snark.ai ")
        if not username:
            logger.debug("Prompting for username.")
            username = click.prompt('Username', type=str)
        username = username.strip()
        if not password:
            logger.debug("Prompting for password.")
            password = click.prompt('Password', type=str, hide_input=True)
        password = password.strip()
        token = AuthClient().get_access_token(username, password)

    TokenManager.set_token(token)
    logger.info("Login Successful.")

@click.command()
def logout():
    """ Logs out of Snark AI"""
    TokenManager.purge_token()


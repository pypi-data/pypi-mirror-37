import click
from snark.log import logger
from snark import config
from snark.client.pod_control import PodControlClient
from snark.cli.auth import login
from snark.token_manager import TokenManager


from subprocess import call
import os
import subprocess
from snark.cli.utils import get_proxy_command

def get_pod_key_path(username, pod_id):
    return os.path.join(config.POD_KEY_DIR_PATH, username, pod_id)

def install_pod_key(username, pod_id, private_key):
    key_file_path = get_pod_key_path(username, pod_id)
    if not os.path.exists(os.path.dirname(key_file_path)):
        os.makedirs(os.path.dirname(key_file_path))
    with open(key_file_path, 'w') as f:
        os.chmod(key_file_path, 0o600)
        f.write(private_key)

@click.command()
@click.argument('pod_id', default='my_pod')
@click.option('--port_forwarding', '-L', default='', help='Port forwarding')
@click.option('--jupyter', '-j', flag_value=True, default=False, help='Jupyter running')
@click.pass_context
def attach(ctx, pod_id, port_forwarding, jupyter):
   """ Connect to a started pod """
   if not TokenManager.is_authenticated():
       ctx.invoke(login)
   connect(pod_id, port_forwarding=port_forwarding, jupyter=jupyter)

def connect(pod_id, port_forwarding="", jupyter=False):
    """ Connect to a started pod """
    logger.info("Connecting to the pod...")
    proxy, address, username, private_key, port = PodControlClient().get_connect_info(pod_id)

    install_pod_key(username, pod_id, private_key)
    key_file_path = get_pod_key_path(username, pod_id)
    if not port_forwarding == "":
        port_forwarding = "-L "+port_forwarding

    ssh_proxy = get_proxy_command(proxy)
    ssh_jupyter = ""
    if jupyter:
        ssh_jupyter = '-L 8888:localhost:8888 jupyter notebook --ip=0.0.0.0 --port=8888'

    command = ('ssh -i "{}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\
               {} {}@{} -p {} {} {}')\
               .format(key_file_path, ssh_proxy, username, address, port, port_forwarding, ssh_jupyter)

    os.system(command)

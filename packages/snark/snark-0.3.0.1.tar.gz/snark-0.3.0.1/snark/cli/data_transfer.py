import click
from snark.log import logger
from snark import config
from snark.client.pod_control import PodControlClient
from snark.cli.connect import get_pod_key_path, install_pod_key
from snark.cli.utils import get_proxy_command

from subprocess import call
import os
import subprocess

@click.command()
@click.argument('pod_id', default='my_pod')
@click.option('--local_path', '-l', default=None, type=str, help='Path to file on local machine.')
@click.option('--remote_path', '-r', default=None, type=str, help='Path to file on the Pod.')
def push(pod_id, local_path, remote_path):
    """ Transfer file to the pod """
    if not pod_id:
        pod_id = click.prompt('Pod ID', type=str)
    pod_id = pod_id.strip()


    if not local_path:
        local_path = click.prompt('Local path', type=str)
    local_path = local_path.strip()


    if not remote_path:
        remote_path = click.prompt('Remote path', type=str)
    remote_path = remote_path.strip()

    proxy, address, username, private_key, port = PodControlClient().get_connect_info(pod_id)
    install_pod_key(username, pod_id, private_key)
    key_file_path = get_pod_key_path(username, pod_id)
    ssh_proxy = get_proxy_command(proxy)

    command = 'scp -i "{}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\
                    {} -P {} {} {}@{}:{} '.format(key_file_path, ssh_proxy,
                                              port, local_path, username, address, remote_path)
    os.system(command)

@click.command()
@click.argument('pod_id', default='my_pod')
@click.option('--remote_path', '-r', default=None, type=str, help='Path to file on the Pod.')
@click.option('--local_path', '-l', default=None, type=str, help='Path to file on local machine.')
def pull(pod_id, remote_path, local_path):
    """ Transfer file from the pod to the localhost """
    if not pod_id:
        pod_id = click.prompt('Pod ID', type=str)
    pod_id = pod_id.strip()


    if not local_path:
        local_path = click.prompt('Local path', type=str)
    local_path = local_path.strip()


    if not remote_path:
        remote_path = click.prompt('Remote path', type=str)
    remote_path = remote_path.strip()

    proxy, address, username, private_key, port = PodControlClient().get_connect_info(pod_id)
    install_pod_key(username, pod_id, private_key)
    key_file_path = get_pod_key_path(username, pod_id)

    ssh_proxy = get_proxy_command(proxy)

    command = 'scp -i "{}" -oStrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                {} -P {} {}@{}:{} {}'.format(key_file_path, ssh_proxy,
                                               port, username, address, remote_path, local_path)
    os.system(command)

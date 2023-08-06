import click
import datetime
from tabulate import tabulate
from random  import randint

from snark.log import logger
from snark import config
from snark.client.pod_control import PodControlClient
from snark.cli.connect import connect
from snark.cli.auth import login
from snark.token_manager import TokenManager


@click.command()
@click.pass_context
def ls(ctx):
    """ List active pods"""
    logger.debug("Listing Pods.")
    if not TokenManager.is_authenticated():
        ctx.invoke(login)

    pods_dict = PodControlClient().list_active()
    pods_list = [
                  [p,
                      datetime.datetime.fromtimestamp(
                                  float(pods_dict[p]['start_time'])
                                      ).strftime('%Y-%m-%d %H:%M:%S'),
                   pods_dict[p]['GPU_spec']]
                for p in pods_dict]
    print (tabulate(pods_list, headers=['Name', 'Time Start', 'GPU spec']))

@click.command()
@click.argument('pod_id', default='')
@click.option('--pod_type', '-t', default='pytorch', type=click.Choice(config.POD_TYPES),
                help='Pod type')
@click.option('--gpu_count', '-g', type=int, default=1, help='Number of GPUs')
@click.option('--port_forwarding', '-L', default='', help='Port forwarding')
@click.option('--jupyter', '-j', flag_value=True, default=False, help='Jupyter running')
@click.option('--gpu_spec', '-s', type=click.Choice(config.GPU_TYPES),
                                  default=config.GPU_TYPES[0],
                                  help='GPU type')
@click.option('--docker_image', '-d', default=None, help='Dockerhub image name for custom pod')
@click.option('--gpu_count', '-g', type=int, default=1, help='Number of GPUs')
@click.option('--ssh/--no-ssh', '-j', default=True, help='Weather to connect to pod after start')
@click.pass_context
def start(ctx, pod_id, pod_type, gpu_count, gpu_spec, port_forwarding, jupyter, docker_image, ssh):
    """ Launch a Snark AI pod"""
    logger.info("Setting up the pod...")

    if not TokenManager.is_authenticated():
        ctx.invoke(login)

    if not pod_id:
        #pod_id = click.prompt('Pod ID', type=str)
        pod_id = "pod_{}".format(''.join(["%s" % randint(0, 9) for num in range(0, 5)]))
    pod_id = pod_id.strip()

    ## check if pod exists
    active_pods = PodControlClient().list_active()
    #FIXME Check if portforwarding is in correct format o/w will create the pod but will fail

    if pod_id not in active_pods:
        pod_type = pod_type.strip()

        PodControlClient().create_pod(pod_id, pod_type, docker_image)
        logger.debug("Successfully created pod {}.".format(pod_id))

        hardware_spec = {"CPU_count": 1, "GPU_count": gpu_count, "GPU_type": gpu_spec}

        timeout = config.DEFAULT_TIMEOUT
        if pod_type == 'custom':
            timeout = config.DEFAULT_TIMEOUT * 10

        PodControlClient().start_pod(pod_id, hardware_spec, timeout=timeout)
        logger.debug("Successfully started pod {}.".format(pod_id))
        if ssh:
            connect(pod_id, jupyter=jupyter, port_forwarding=port_forwarding)
    else:
        logger.info("Pod with ID `{}` is already running. Please use `snark attach {}` to reattach.".format(pod_id, pod_id))

def terminate(pod_id):
    """ Terminate the given pod"""
    logger.debug("Terminating pod.")
    pod_id = pod_id.strip()

    PodControlClient().terminate_pod(pod_id)
    logger.debug("Successfully terminated pod {}.".format(pod_id))


@click.command()
@click.argument('pod_id')
@click.pass_context
def stop(ctx, pod_id):
    """ Stop the given pod """
    logger.info("Stopping pod...")
    if not TokenManager.is_authenticated():
        ctx.invoke(login)
    if not pod_id:
        pod_id = click.prompt('Pod ID', type=str)
    pod_id = pod_id.strip()

    PodControlClient().stop_pod(pod_id)
    terminate(pod_id)
    logger.debug("Successfully stopped pod {}.".format(pod_id))

import json

import snark
from snark import config
from snark.log import logger
from snark.client.base import SnarkHttpClient
from snark.exceptions import SnarkException

class PodControlClient(SnarkHttpClient):
    """
    Controlling Snark Pods through rest api
    """
    def __init__(self):
        super(PodControlClient, self).__init__()

    def create_pod(self, pod_id, pod_type, custom_docker_image):
        response = self.request('GET', config.CREATE_POD_REST_SUFFIX,
                                json={"pod_id": pod_id,
                                      "pod_type": pod_type,
                                      "custom_docker_image": custom_docker_image})

    def terminate_pod(self, pod_id):
        response = self.request('GET', config.TERMINATE_POD_REST_SUFFIX,
                                json={"pod_id": pod_id})

    def start_pod(self, pod_id, hardware_spec, timeout=config.DEFAULT_TIMEOUT):
        response = self.request('GET', config.START_POD_REST_SUFFIX,
                json={"pod_id": pod_id, "hardware_spec": json.dumps(hardware_spec)}, timeout=timeout)

    def stop_pod(self, pod_id):
        response = self.request('GET', config.STOP_POD_REST_SUFFIX,
                                json={"pod_id": pod_id})

    def get_connect_info(self, pod_id):
        response = self.request('GET', config.GET_CONNECT_INFO_REST_SUFFIX,
                                json={"pod_id": pod_id})
        response = response.json()
        return (response['is_proxy'],
               response['address'],
               response['username'],
               response['private_key'],
               response['port'])

    def list_active(self):
        response = self.request('GET', config.LIST_ACTIVE_PODS_REST_SUFFIX)
        active_pods_json = response.json()['active_pods']
        active_pods = json.loads(active_pods_json)
        return active_pods

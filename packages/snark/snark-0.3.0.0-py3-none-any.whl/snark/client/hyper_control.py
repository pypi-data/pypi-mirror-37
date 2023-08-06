import json

import snark
from snark import config
from snark.log import logger
from snark.client.base import SnarkHttpClient
from snark.exceptions import SnarkException

class HyperControlClient(SnarkHttpClient):
    """
    Controlling Snark Pods through rest api
    """
    def __init__(self):
        super(HyperControlClient, self).__init__()

    def upload(self, descriptor):
        files = {"descriptor": descriptor}

        response = self.request(
            'POST', config.UP_DESCRIPTOR_SUFFIX,
            endpoint=config.SNARK_HYPER_ENDPOINT,
            files=files
        )
        return response.json()

    def down(self, descriptor):
        files = {"descriptor": descriptor}
        response = self.request(
            'POST', config.DOWN_DESCRIPTOR_SUFFIX,
            endpoint=config.SNARK_HYPER_ENDPOINT,
            files=files
        )
        return response.json()

    def list(self):
        response = self.request(
            'GET', config.LIST_EXPERIMENTS_SUFFIX,
            endpoint=config.SNARK_HYPER_ENDPOINT
        )
        return response.json()

    def list_task(self, experiment_id):
        data = {"experiment_id": experiment_id}
        response = self.request(
            'GET', config.LIST_EXPERIMENT_SUFFIX,
            endpoint=config.SNARK_HYPER_ENDPOINT,
            json=data
        )
        return response.json()

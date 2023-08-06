import websocket
import time
import json
import requests
import uuid
import numpy as np
from datetime import datetime

from snark.token_manager import TokenManager
from snark.infer.message_processor import construct_infer_message, parse_data_message

class SnarkModel(object):
    """Snark Infer model"""

    def __init__(self, model_name):
        self.host = 'core.snark.ai'
        self.ws_port = 10004
        self.endpoint = "ws://{}:{}".format(self.host, self.ws_port)
        self.model_name = model_name
        self.input_shape = None
        self.output_shape = None
        self.model_info = {}
        self.task_id = uuid.uuid4()
        global snark_token

        self.token = TokenManager.get_token()
        self.ws = websocket.create_connection(self.endpoint)
        self.ws.settimeout(300)  # 300 secs timeout for receiving data
        self._connect()

    def __del__(self):
        try:
            self.ws.close()
        except:
            pass

    def _connect(self):
        # authentication message
        self.ws.send(json.dumps({"api_key": self.token,
                                 "payload": {
                                     "model": "/" + self.model_name,
                                     "task_id": str(self.task_id)
                                 }
                                 })
                     )
        reply = self.ws.recv()  # blocking call
        try:
            r = json.loads(reply)
        except Exception as e:
            raise Exception(
                "Failed to create a model connection. Server side error.")

        if (not "status" in r) or (r["status"] != "successful"):
            if not "description" in r:
                raise Exception(
                    "Failed to create a model connection. Server side error.")

            raise Exception(
                "Failed to create model connection. {}".format(r["description"]))
        else:
            self.model_info = r["model_info"]
            self.input_shape = tuple(json.loads(
                self.model_info["input_shape"]))
            self.output_shape = tuple(json.loads(
                self.model_info["output_shape"]))

    def infer(self, np_input, verbose=False):
        assert (np_input.shape == self.input_shape) or \
               (np_input[np.newaxis, ...].shape == self.input_shape)

        if (np_input[np.newaxis, ...].shape == self.input_shape):
            np_input = np_input[np.newaxis, ...]
        try:
            infer_message = construct_infer_message(np_input)
        except Exception as e:
            raise e

        self.ws.send(infer_message, opcode=websocket.ABNF.OPCODE_BINARY)

        if verbose:
            sent_time = datetime.now()
            print('[{}] Request sent...'.format(sent_time))
        try:
            result_raw = self.ws.recv()
        except Exception as e:
            raise Exception(
                "Failed to receive result from the server. Please try again.")


        if verbose:
            received_time = datetime.now()
            elapsed_time = received_time - sent_time
            elapsed_secs = elapsed_time.total_seconds()
            print("[{}] Reply received. Time elapsed: {} sec".format(
                received_time, elapsed_secs))

        result_np = parse_data_message(result_raw, self.output_shape)
        return result_np

def model(model_name):
    return SnarkModel(model_name)


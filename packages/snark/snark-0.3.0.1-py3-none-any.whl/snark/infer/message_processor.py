import numpy as np
import uuid
import json

def construct_infer_message(numpy_array):
    imgdata = numpy_array.ravel().tobytes()
    return imgdata

def parse_data_message(imgdata, dims):
    # through reasonable exception if message is of bad format
    np_array = np.fromstring(imgdata, dtype=np.float32).reshape(*dims)
    return np_array

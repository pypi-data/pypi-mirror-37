import os

curr_path = os.path.dirname(os.path.abspath(__file__))

TOKEN_FILE_PATH = os.path.expanduser("~/.snarkai/token")
POD_KEY_DIR_PATH = os.path.expanduser("~/.snarkai/pod_keys")

SNARK_REST_ENDPOINT  = "https://controller.snark.ai"
SNARK_HYPER_ENDPOINT = "https://hyper.snark.ai:5000"

UP_DESCRIPTOR_SUFFIX            = "/api/v1/experiment/up"
DOWN_DESCRIPTOR_SUFFIX          = "/api/v1/experiment/down"
LIST_EXPERIMENTS_SUFFIX         = "/api/v1/experiment/all"
LIST_EXPERIMENT_SUFFIX          = "/api/v1/experiment/id"

GET_TOKEN_REST_SUFFIX     = "/api/v1/get_token"
CHECK_TOKEN_REST_SUFFIX   = "/api/v1/check_token"

CREATE_POD_REST_SUFFIX       = "/api/v1/pod/create"
TERMINATE_POD_REST_SUFFIX    = "/api/v1/pod/terminate"
START_POD_REST_SUFFIX        = "/api/v1/pod/start"
STOP_POD_REST_SUFFIX         = "/api/v1/pod/stop"
GET_CONNECT_INFO_REST_SUFFIX = "/api/v1/pod/connect_info"
LIST_ACTIVE_PODS_REST_SUFFIX = "/api/v1/pod/ls"
ADMIN_STOP_POD_REST_SUFFIX       = "/api/v1/admin/pod/stop"
ADMIN_TERMINATE_POD_REST_SUFFIX  = "/api/v1/admin/pod/terminate"
ADMIN_LS_ALL_REST_SUFFIX         = "/api/v1/admin/pod/ls_all"

POD_TYPES = ['pytorch', 'tensorflow', 'mxnet', 'caffe', 'fast.ai', 'custom']
GPU_TYPES = ['P106', '1080', '1070', 'Q4000']

DEFAULT_TIMEOUT = 170

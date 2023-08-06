import os
from snark import config

def set_up_file(path):
    full_path = os.path.expanduser(path)
    dir_name  = os.path.dirname(full_path)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #create an empty file
    with open(path, 'a+'):
        pass

set_up_file(config.TOKEN_FILE_PATH)

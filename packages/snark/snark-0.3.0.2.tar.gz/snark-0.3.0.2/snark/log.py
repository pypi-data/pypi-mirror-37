import logging
import sys

logger = logging.getLogger('snark')
def configure_logger(debug):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format='%(message)s',
                        level=log_level,
                        stream=sys.stdout)


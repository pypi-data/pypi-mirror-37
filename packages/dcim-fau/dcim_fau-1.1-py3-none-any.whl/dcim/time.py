from time import time, sleep
from dcim.configuration import get_config
import logging

logger = logging.getLogger(__name__)


# wait for specified (conf.yaml) interval value
def wait(start):
    interval = get_config('chron')['COLL_INTERVAL']
    logger.info('waiting {0} seconds'.format(interval-(time()-start)))
    while time() - start < interval:
        sleep(.1)

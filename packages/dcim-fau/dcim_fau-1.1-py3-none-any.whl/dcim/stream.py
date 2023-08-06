from walrus import *
from dcim.configuration import get_config
import logging

logger = logging.getLogger(__name__)


# initializes with a Redis stream connection, accepts packets
class StreamEngine:
    stream = 0
    packet_size = 0
    packet_count = 0

    def __init__(self):
        logger.info('opening stream..')
        stream_config = get_config('stream')
        host = stream_config['STREAM_HOST']
        password = stream_config['STREAM_PASS']
        stream = stream_config['STREAM_ID']
        self.packet_size = stream_config['STREAM_PACKET']

        db = Database(
            host=host,
            port=6379,
            password=password,
            db=0
        )
        self.stream = db.Stream(stream)

    # accepts a response blob, creates 'packets', and adds to stream
    # as specified in config, clears response blob
    def add(self, response_blob):
        logger.info('adding data to stream...')

        packet = []

        for index, entry in enumerate(response_blob):
            packet.append(entry)

            if index == self.packet_size:
                self.packet_count += 1
                self.stream.add({self.packet_count: packet})
                logger.info('packet_id {0} added to stream'.format(self.packet_count))
                packet.clear()

        if packet:
            self.packet_count += 1
            self.stream.add({self.packet_count: packet})
            logger.info('packet_id {0} added to stream'.format(self.packet_count))

        response_blob.clear()

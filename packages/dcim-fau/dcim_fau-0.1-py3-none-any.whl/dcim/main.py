from dcim.snmp import SNMPEngine
from dcim.stream import StreamEngine
import dcim.builder as build
from dcim.configuration import get_config
from dcim.time import wait
from time import time
import logging

logging.basicConfig(filename='snmp.log', level=logging.DEBUG)


def run():

    # collecting data necessary for process loop
    config_chron = get_config('chron')
    targets_blob = get_config('targets')

    snmp_targets = build.racks(targets_blob)

    # initializing engines
    snmp_engine = SNMPEngine(snmp_targets)
    stream_engine = StreamEngine()

    while True:
        interval_start = time()

        snmp_engine.enqueue_requests()
        results = snmp_engine.process_requests()

        stream_engine.add(results)
        results.clear()

        wait(interval_start, config_chron['COLL_INTERVAL'])

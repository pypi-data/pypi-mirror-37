from dcim.snmp import SNMPEngine
from dcim.stream import StreamEngine
import dcim.builder as build
from dcim.time import wait
from time import time
import logging

logging.basicConfig(filename='snmp.log', level=logging.DEBUG)


def run():
    snmp_targets = build.racks()

    # initializing engines
    snmp_engine = SNMPEngine(snmp_targets)
    stream_engine = StreamEngine()

    while True:
        interval_start = time()

        snmp_engine.enqueue_requests()
        results = snmp_engine.process_requests()

        stream_engine.add(results)
        results.clear()

        wait(interval_start)

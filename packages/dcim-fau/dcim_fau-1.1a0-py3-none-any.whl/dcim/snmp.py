from pysnmp.hlapi.asyncio import (
    getCmd,
    CommunityData,
    UdpTransportTarget,
    SnmpEngine,
    ContextData,

)
from pysnmp.smi import view
import asyncio
import logging
from dcim.configuration import get_config

logger = logging.getLogger(__name__)


# Adaption of PySNMP Engine, performs all SNMP processing asynchronously
class SNMPEngine:
    requests = []
    targets = []
    results = []
    community_string = ''
    timeout = 0
    snmpEngine = 0
    loop = 0
    queue = 0
    mibViewController = 0

    def __init__(self, targets):
        self.requests = []
        self.targets = targets
        self.results = []
        self.community_string = get_config('snmp')['COMM_STRING']
        self.timeout = get_config('snmp')['TIMEOUT']
        self.snmpEngine = SnmpEngine()
        self.mibBuilder = self.snmpEngine.getMibBuilder()
        self.mibViewController = view.MibViewController(self.mibBuilder)
        self.loop = asyncio.get_event_loop()

    # process a single SNMP request asynchronously, requires host and snmp_object
    async def send_snmp_request(self, host, target):

        response = await getCmd(
            self.snmpEngine,
            CommunityData(self.community_string, mpModel=1),
            UdpTransportTarget((host, 161)),
            ContextData(),
            target,
        )

        error_indication, error_status, error_index, varbinds = response

        if error_indication:
            logger.warning('%s with this asset: %s', error_indication, host)
            return

        elif error_status:
            logger.warning(
                '%s at %s',
                error_status.prettyPrint(),
            )
            return

        else:
            return varbinds[0]

    # build loop tasks from attached target data
    # with metadata appended
    def enqueue_requests(self):
        logger.info('enqueueing requests..')

        for target in self.targets:
            for equipment in target.contains:
                for oid_obj in equipment.oid_obj_array:

                    # appending parent equipment data label to oid metadata array for later organization
                    metadata_dict = oid_obj.get_metadata_dict()
                    metadata_dict.update({'label': equipment.get_label()})

                    # appending targets to requests queue
                    self.requests.append({
                        self.loop.create_task(
                            self.send_snmp_request(equipment.ip, oid_obj.snmp_object)
                        ):
                            metadata_dict
                    })

    def process_requests(self):
        logger.info('processing request queue..')
        response_data = []
        failures = 0

        for request in self.requests:
            for snmp_request, metadata in request.items():
                response = self.loop.run_until_complete(snmp_request)

                if response:

                    payload = str(response).split('=', 1)[1].lstrip()

                    # did our formatted payload response create an integer? if so, success
                    try:
                        payload = int(payload) / metadata['divisor']

                        metadata.update({'payload': payload})
                    except ValueError:
                        logger.warning('failed integer division for payload {0}'.format(payload))
                        failures += 1

                else:
                    failures += 1

        if failures:
            logger.warning('{0} snmp attempts not returned from snmp'.format(failures))

        self.requests.clear()
        return response_data

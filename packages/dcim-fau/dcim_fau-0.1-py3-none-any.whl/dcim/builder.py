from pysnmp.hlapi.asyncio import (
    ObjectType,
    ObjectIdentity
)
from dcim.configuration import get_config
import logging

logger = logging.getLogger(__name__)


# accepts config target data, returns array of Rack objects
# on init, ea rack object initializes their containing equipment
def racks(targets_blob):
    logger.info('building rack table..')

    snmp_targets = []
    id = 0

    # getting individual equipment profile, row from config
    for snmp_target_label, snmp_target in targets_blob.items():

        id += 1
        equipment = snmp_target['equipment']
        row = snmp_target['row']

        logger.info('rack ' + row + str(id) + ' initialized')
        snmp_targets.append(Rack(id, equipment, row))

    return snmp_targets


# accepts config oid data relative to equipment type.
# returns array of Oid objects containing value and divisor
def oids(oid_array):
    oid_obj_array = []

    for oid_entry in oid_array:

        type = list(oid_entry.keys())[0]

        # handling layered dictionary and lists from config
        oid_entry = oid_entry.popitem()[1]

        value = oid_entry['value']
        divisor = oid_entry['divisor']

        oid_obj = Oid(value, divisor, type)

        oid_obj_array.append(oid_obj)

    return oid_obj_array


# constructor accepts equipment array, processes each one to bind snmp data
class Rack:
    contains = []
    id = 0
    row = 0

    def __init__(self, id, rack_equipment, row):
        self.id = id
        self.row = row

        for equipment in rack_equipment:
            ip = equipment['ip']
            equipment_type = equipment['type']

            oid_array = get_config('oids')[equipment_type]
            oid_obj_array = oids(oid_array)

            self.contains.append(
                Equipment(
                    equipment_type,
                    ip,
                    row,
                    id,
                    oid_obj_array
                )
            )


class Equipment:
    equipment_type = ''
    ip = ''
    sensor_id = ''
    oid_array = []
    rack = 0
    row = 0

    def __init__(self, equipment_type, ip, row, rack, oid_obj_array):
        self.equipment_type = equipment_type
        self.ip = ip
        self.oid_array = oid_obj_array
        self.rack = rack
        self.row = row
        self.sensor_id = ''

    def get_label(self):
        label = str(self.row) + str(self.rack) + str(self.equipment_type)
        return label


# contains data necessary for SNMP request object
class Oid:
    value = 0
    divisor = 0
    type = ''
    snmp_request = 0

    def __init__(self, value, divisor, type):
        self.value = value
        self.divisor = divisor
        self.type = type
        self.snmp_object = self.snmp_object()

    def get_oid(self):
        return self.value

    def get_divisor(self):
        return self.divisor

    def get_type(self):
        return self.type

    def get_snmp_object(self):
        return self.snmp_object

    def get_metadata_dict(self):
        metadata_array = {
                            'type': self.get_type(),
                            'divisor': self.get_divisor()
        }
        return metadata_array

    def snmp_object(self):
        return ObjectType(ObjectIdentity(self.get_oid()))

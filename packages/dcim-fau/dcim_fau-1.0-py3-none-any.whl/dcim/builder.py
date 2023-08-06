from pysnmp.hlapi.asyncio import (
    ObjectType,
    ObjectIdentity
)
from dcim.configuration import get_config
import logging

logger = logging.getLogger(__name__)


# accepts config target data, returns array of Rack objects
# on init, ea rack object initializes their containing equipment
def racks():
    logger.info('building rack table..')

    targets_blob = get_config('targets')
    snmp_targets = []
    rack_id = 0

    # getting individual equipment profile, row from config
    for snmp_target_label, snmp_target in targets_blob.items():

        rack_id += 1
        equipment = snmp_target['equipment']
        row = snmp_target['row']

        logger.info('rack ' + row + str(rack_id) + ' initialized')
        snmp_targets.append(Rack(rack_id, equipment, row))

    return snmp_targets


# constructor accepts equipment array, processes each one to bind snmp data
class Rack:
    contains = []
    rack_id = 0
    row = 0

    def __init__(self, rack_id, rack_equipment, row):
        self.rack_id = rack_id
        self.row = row
        self.contains = []
        self.build_equipment(rack_equipment)

    def build_equipment(self, rack_equipment):
        for equipment in rack_equipment:
            ip = equipment['ip']
            equipment_type = equipment['type']

            try:
                sensor_id = equipment['sensor']
            except KeyError:
                sensor_id = 0

            self.contains.append(
                Equipment(
                    equipment_type,
                    ip,
                    self.row,
                    self.rack_id,
                    sensor_id
                )
            )


class Equipment:
    equipment_type = ''
    oid_obj_array = []
    ip = ''
    rack = 0
    row = 0
    sensor = 0

    def __init__(self, equipment_type, ip, row, rack, sensor):
        self.equipment_type = equipment_type
        self.oid_obj_array = []
        self.ip = ip
        self.row = row
        self.rack = rack
        self.sensor = sensor
        self.build_oids()

    def get_label(self):
        label = str(self.row) + str(self.rack) + str(self.equipment_type)
        return label

    # accepts config oid data relative to equipment type.
    # returns array of Oid objects containing value and divisor
    def build_oids(self):
        oid_array = get_config('oids')[self.equipment_type]

        for oid_entry in oid_array:
            type = list(oid_entry.keys())[0]

            # handling layered dictionary and lists from config
            oid_entry = oid_entry.popitem()[1]

            value = oid_entry['value']
            divisor = oid_entry['divisor']

            # sensor check
            if self.sensor:
                value = str(value) + '.' + str(self.sensor)

            oid_obj = Oid(value, divisor, type)

            self.oid_obj_array.append(oid_obj)


# contains data necessary for SNMP request object
class Oid:
    value = 0
    divisor = 1
    type = ''

    def __init__(self, value, divisor, type):
        self.value = value
        self.divisor = divisor
        self.type = type
        self.snmp_object = self.snmp_object()

    def get_divisor(self):
        return self.divisor

    def get_type(self):
        return self.type

    def get_metadata_dict(self):
        metadata_array = {
                            'type': self.get_type(),
                            'divisor': self.get_divisor()
        }
        return metadata_array

    def snmp_object(self):
        return ObjectType(
            ObjectIdentity(
                self.value
            ))

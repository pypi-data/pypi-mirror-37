import re
import socket
from snmpsim.error import NoDataNotification
from snmpsim.record.snmprec import SnmprecRecord


class SnmpRecord(SnmprecRecord):
    SNMP_TYPE_MAP = {"2": "Integer",
                     "4": "OctetString",
                     "5": "Null",
                     "6": "ObjectID",
                     "64": "IpAddress",
                     "65": "Counter",
                     "66": "Gauge",
                     "67": "TimeTicks",
                     "68": "Opaque",
                     "70": "Counter64"}

    def formatValue(self, oid, value, **context):
        oid, snmp_type, snmp_value = SnmprecRecord.formatValue(
            self, oid, value
        )

        if 'stopFlag' in context and context['stopFlag']:
            raise NoDataNotification()
        type = self.SNMP_TYPE_MAP.get(re.sub("\D*", "", snmp_type))
        if not type:
            print "Failed to parse record: {}, {}, {}".format(oid, snmp_type, snmp_value)
        if "string" in type.lower() and "x" not in snmp_type:
            snmp_value = snmp_value.encode("hex")
        if "64" in snmp_type:
            ip = snmp_value
            if "x" in snmp_type:
                ip = snmp_value.decode("hex")
            value = socket.inet_ntoa(ip)
        else:
            value = self.get_snmp_value(type, snmp_value)
        return oid, type, value

    def get_snmp_value(self, snmp_type, snmp_value):
        result_value = str(snmp_value)
        if not snmp_value.startswith("0x") and snmp_value and "octetstring" in snmp_type.lower():
            result_value = "0x" + snmp_value
        elif "timeticks" in snmp_type.lower():
            try:
                time_ticks = int(snmp_value) / 100
                minutes, seconds = divmod(time_ticks, 60)
                hours, minutes = divmod(minutes, 60)
                result_value = "{} hours, {} minutes, {} seconds.".format(hours, minutes, seconds)
            except:
                result_value = "0 hours, 0 minutes, 0 seconds."
        return result_value

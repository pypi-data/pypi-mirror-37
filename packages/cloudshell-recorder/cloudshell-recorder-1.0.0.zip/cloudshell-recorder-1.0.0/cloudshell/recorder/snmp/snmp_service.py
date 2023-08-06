from cloudshell.recorder.model.base_snmp_parameters import BaseSnmpParameters
from cloudshell.recorder.snmp.snmp_recorder import SnmpRecorder


class SnmpService(object):
    def __init__(self, snmp_parameters):
        """

        :param BaseSnmpParameters snmp_parameters: Snmp parameters object
        """
        self._snmp_parameters = snmp_parameters

    def __enter__(self):
        return SnmpRecorder(self._snmp_parameters)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._snmp_parameters.close_snmp_engine_dispatcher()

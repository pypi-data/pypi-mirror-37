from cloudshell.recorder.model.base_snmp_parameters import BaseSnmpParameters, config


class SnmpV2Parameters(BaseSnmpParameters):
    def __init__(self, ip, snmp_community, snmp_version="2", port=161, is_ipv6=False, timeout=2000, retry_count=2,
                 get_bulk_flag=False,
                 continue_on_errors=0, get_bulk_repetitions=25, v3_context_engine_id=None, v3_context=''):
        self._user = 'agt'
        self._sec_level = 'noAuthNoPriv'
        self._snmp_version = 0
        if "2" in snmp_version:
            self._snmp_version = 1
        super(SnmpV2Parameters, self).__init__(ip, port, is_ipv6, timeout, retry_count, get_bulk_flag,
                                               continue_on_errors, get_bulk_repetitions, v3_context_engine_id,
                                               v3_context)
        config.addV1System(
            self._snmp_engine, self._user, snmp_community
        )
        if self.get_bulk_flag and (not snmp_version or snmp_version == "1"):
            self.get_bulk_flag = False

    @property
    def get_security(self):
        return self._sec_level

    @property
    def get_user(self):
        return self._user

    @property
    def get_snmp_version(self):
        return self._snmp_version

from unittest import TestCase

from mock import patch, MagicMock, PropertyMock

from cloudshell.recorder.model.snmp_v2_parameters import SnmpV2Parameters


class TestSnmpV2Params(TestCase):
    IP = "1.1.1.1"
    SNMP_COMMUNITY = "test"

    @patch("cloudshell.recorder.model.snmp_v2_parameters.config")
    @patch("__builtin__.super", create=True, return_value=MagicMock())
    @patch("cloudshell.recorder.model.snmp_v2_parameters.SnmpV2Parameters._snmp_engine", create=True, new_callable=PropertyMock,
           return_value="")
    @patch("cloudshell.recorder.model.snmp_v2_parameters.SnmpV2Parameters.get_bulk_flag", create=True, new_callable=PropertyMock)
    def test_init(self, bulk_rep_mock, engine_mock, super_mock, config_mock):
        # Setup
        version = "1"
        # Strange pysnmp snmp version conversion
        snmp_version = 0
        sec_level = 'noAuthNoPriv'
        user = 'agt'
        port = 162
        is_ipv6 = True
        timeout = 1
        retry_count = 1
        get_bulk_flag = True
        continue_on_errors = 1
        get_bulk_repetitions = 2
        v3_context_engine_id = MagicMock()
        v3_context = MagicMock()
        bulk_rep_mock.return_value = get_bulk_flag

        # Act
        params = SnmpV2Parameters(ip=self.IP, snmp_community=self.SNMP_COMMUNITY, snmp_version=version, port=port,
                                  is_ipv6=is_ipv6, timeout=timeout, retry_count=retry_count,
                                  get_bulk_flag=get_bulk_flag, continue_on_errors=continue_on_errors,
                                  get_bulk_repetitions=get_bulk_repetitions, v3_context_engine_id=v3_context_engine_id,
                                  v3_context=v3_context)

        # Assert
        super_mock.assert_called_once_with(SnmpV2Parameters, params)
        self.assertEqual(snmp_version, params.get_snmp_version)
        self.assertEqual(sec_level, params.get_security)
        self.assertEqual(user, params.get_user)


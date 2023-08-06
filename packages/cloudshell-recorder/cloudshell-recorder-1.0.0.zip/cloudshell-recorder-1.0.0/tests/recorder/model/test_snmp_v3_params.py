from unittest import TestCase

from mock import patch, MagicMock, PropertyMock

from cloudshell.recorder.model.snmp_v3_parameters import SnmpV3Parameters


class TestSnmpV3Params(TestCase):
    IP = "1.1.1.1"
    SNMP_COMMUNITY = "test"

    @patch("cloudshell.recorder.model.snmp_v3_parameters.config")
    @patch("__builtin__.super", create=True, return_value=MagicMock())
    @patch("cloudshell.recorder.model.snmp_v3_parameters.SnmpV3Parameters._snmp_engine", create=True,
           new_callable=PropertyMock,
           return_value="")
    @patch("cloudshell.recorder.model.snmp_v3_parameters.SnmpV3Parameters.get_bulk_flag", create=True,
           new_callable=PropertyMock)
    def test_init(self, bulk_rep_mock, engine_mock, super_mock, config_mock):
        # Setup
        snmp_version = 3
        sec_level = 'noAuthNoPriv'
        user = 'agt'
        password = None
        private_key = None
        auth_protocol = "SHA"
        priv_protocol = "DES"
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
        params = SnmpV3Parameters(ip=self.IP, v3_user=user, v3_auth_key=password, v3_priv_key=private_key,
                                  v3_auth_proto=auth_protocol, v3_priv_proto=priv_protocol, port=port,
                                  is_ipv6=is_ipv6, timeout=timeout, retry_count=retry_count,
                                  get_bulk_flag=get_bulk_flag, continue_on_errors=continue_on_errors,
                                  get_bulk_repetitions=get_bulk_repetitions, v3_context_engine_id=v3_context_engine_id,
                                  v3_context=v3_context)

        # Assert
        super_mock.assert_called_once_with(SnmpV3Parameters, params)
        self.assertEqual(snmp_version, params.get_snmp_version)
        self.assertEqual(sec_level, params.get_security)
        self.assertEqual(user, params.get_user)

    @patch("cloudshell.recorder.model.snmp_v3_parameters.config")
    @patch("__builtin__.super", create=True, return_value=MagicMock())
    @patch("cloudshell.recorder.model.snmp_v3_parameters.SnmpV3Parameters._snmp_engine", create=True,
           new_callable=PropertyMock,
           return_value="")
    def test_sec_level_auth(self, engine_mock, super_mock, config_mock):
        # Setup
        snmp_version = 3
        sec_level = 'authNoPriv'
        user = 'agt'
        password = "pass"
        private_key = None
        auth_protocol = "SHA"
        priv_protocol = "DES"

        # Act
        params = SnmpV3Parameters(ip=self.IP, v3_user=user, v3_auth_key=password, v3_priv_key=private_key,
                                  v3_auth_proto=auth_protocol, v3_priv_proto=priv_protocol)

        # Assert
        super_mock.assert_called_once_with(SnmpV3Parameters, params)
        self.assertEqual(snmp_version, params.get_snmp_version)
        self.assertEqual(sec_level, params.get_security)
        self.assertEqual(user, params.get_user)

    @patch("cloudshell.recorder.model.snmp_v3_parameters.config")
    @patch("__builtin__.super", create=True, return_value=MagicMock())
    @patch("cloudshell.recorder.model.snmp_v3_parameters.SnmpV3Parameters._snmp_engine", create=True,
           new_callable=PropertyMock,
           return_value="")
    def test_sec_level_priv(self, engine_mock, super_mock, config_mock):
        # Setup
        snmp_version = 3
        sec_level = 'authPriv'
        user = 'agt'
        password = "pass"
        private_key = "pass"
        auth_protocol = "SHA"
        priv_protocol = "DES"

        # Act
        params = SnmpV3Parameters(ip=self.IP, v3_user=user, v3_auth_key=password, v3_priv_key=private_key,
                                  v3_auth_proto=auth_protocol, v3_priv_proto=priv_protocol)

        # Assert
        super_mock.assert_called_once_with(SnmpV3Parameters, params)
        self.assertEqual(snmp_version, params.get_snmp_version)
        self.assertEqual(sec_level, params.get_security)
        self.assertEqual(user, params.get_user)
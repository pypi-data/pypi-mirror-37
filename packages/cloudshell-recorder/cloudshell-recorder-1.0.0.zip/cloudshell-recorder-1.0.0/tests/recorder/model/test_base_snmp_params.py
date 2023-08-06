from unittest import TestCase

from mock import patch, MagicMock, PropertyMock

from cloudshell.recorder.model.base_snmp_parameters import BaseSnmpParameters


class TestBaseSnmpParams(TestCase):
    IP = "1.1.1.1"
    SNMP_COMMUNITY = "test"

    @patch("cloudshell.recorder.model.base_snmp_parameters.engine")
    @patch("cloudshell.recorder.model.base_snmp_parameters.config")
    @patch("cloudshell.recorder.model.base_snmp_parameters.udp")
    @patch("cloudshell.recorder.model.base_snmp_parameters.udp6")
    @patch("cloudshell.recorder.model.base_snmp_parameters.univ")
    @patch("cloudshell.recorder.model.base_snmp_parameters.socket")
    @patch("cloudshell.recorder.model.base_snmp_parameters.sys")
    def test_init(self, sys_mock, socket_mock, pyasn1_mock, pysnmp_udp6_mock, pysnmp_udp_mock, pysnmp_config_mock,
                  pysnmp_engine_mock):
        # Setup
        port = 162
        is_ipv6 = True
        timeout = 1
        retry_count = 1
        get_bulk_flag = True
        continue_on_errors = 1
        get_bulk_repetitions = 2
        v3_context_engine_id = MagicMock()
        v3_context = MagicMock()

        # Act
        params = BaseSnmpParameters(ip=self.IP, port=port,
                                    is_ipv6=is_ipv6, timeout=timeout, retry_count=retry_count,
                                    get_bulk_flag=get_bulk_flag, continue_on_errors=continue_on_errors,
                                    get_bulk_repetitions=get_bulk_repetitions,
                                    v3_context_engine_id=v3_context_engine_id,
                                    v3_context=v3_context)

        # Assert
        pysnmp_engine_mock.SnmpEngine.assert_called_once()
        self.assertEqual(pysnmp_engine_mock.SnmpEngine.return_value, params.snmp_engine)
        self.assertEqual(None, params.close_snmp_engine_dispatcher())
        pysnmp_engine_mock.SnmpEngine.return_value.transportDispatcher.closeDispatcher.assert_called_once()

    @patch("cloudshell.recorder.model.base_snmp_parameters.engine")
    @patch("cloudshell.recorder.model.base_snmp_parameters.config")
    @patch("cloudshell.recorder.model.base_snmp_parameters.udp")
    @patch("cloudshell.recorder.model.base_snmp_parameters.udp6")
    @patch("cloudshell.recorder.model.base_snmp_parameters.univ")
    @patch("cloudshell.recorder.model.base_snmp_parameters.socket")
    @patch("cloudshell.recorder.model.base_snmp_parameters.sys")
    def test_init_with_context(self, sys_mock, socket_mock, pyasn1_mock, pysnmp_udp6_mock, pysnmp_udp_mock, pysnmp_config_mock,
                  pysnmp_engine_mock):
        # Setup
        port = 162
        is_ipv6 = True
        timeout = 1
        retry_count = 1
        get_bulk_flag = True
        continue_on_errors = 1
        get_bulk_repetitions = 2
        v3_context_engine_id = "0xsomething"
        v3_context = "0xsomething"

        # Act
        params = BaseSnmpParameters(ip=self.IP, port=port,
                                    is_ipv6=is_ipv6, timeout=timeout, retry_count=retry_count,
                                    get_bulk_flag=get_bulk_flag, continue_on_errors=continue_on_errors,
                                    get_bulk_repetitions=get_bulk_repetitions,
                                    v3_context_engine_id=v3_context_engine_id,
                                    v3_context=v3_context)

        # Assert
        pysnmp_engine_mock.SnmpEngine.assert_called_once()
        self.assertEqual(pysnmp_engine_mock.SnmpEngine.return_value, params.snmp_engine)
        self.assertEqual(None, params.close_snmp_engine_dispatcher())
        pysnmp_engine_mock.SnmpEngine.return_value.transportDispatcher.closeDispatcher.assert_called_once()

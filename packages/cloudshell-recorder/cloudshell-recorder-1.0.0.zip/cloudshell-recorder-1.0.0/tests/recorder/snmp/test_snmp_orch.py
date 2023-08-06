from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.snmp.snmp_orchestrator import SNMPOrchestrator


class TestSnmpOrchestrator(TestCase):
    @patch("cloudshell.recorder.snmp.snmp_orchestrator.click")
    @patch("cloudshell.recorder.snmp.snmp_orchestrator.SnmpService")
    def test_create_recording(self, snmp_service_mock, click_mock):
        # Setup
        snmp_orchestrator = SNMPOrchestrator(MagicMock())
        response_list = ["1.3.6.1.2.1.1.2.1.3.6.1.4.1.4", "2"]
        snmp_recorder_mock = MagicMock()
        snmp_recorder_mock.create_snmp_record.side_effect = [["1.3.6.1.2.1.1.2.1.3.6.1.4.1.4"], ["2"], ["3"], ["4"],
                                                             ["5"]]
        snmp_service_mock.return_value.__enter__.return_value = snmp_recorder_mock

        # Act
        result = snmp_orchestrator.create_recording()

        # Assert
        self.assertEqual(result, response_list)

    @patch("cloudshell.recorder.snmp.snmp_orchestrator.click")
    @patch("cloudshell.recorder.snmp.snmp_orchestrator.SnmpService")
    def test_create_recording_custom_oid(self, snmp_service_mock, click_mock):
        # Setup
        oids_list = ["1.1.1.1.1.1", "22.2.2.2.2.test", "#3.3.3.3.3", "3.3.3.3.3#text to skip", ".3.3.3.3.3"]
        snmp_orchestrator = SNMPOrchestrator(MagicMock(), template_oid_list=oids_list)
        response_list = ["1.3.6.1.2.1.1.2.1.3.6.1.4.1.4", "2", "3", "4", "5", "6"]
        snmp_recorder_mock = MagicMock()
        snmp_recorder_mock.create_snmp_record.side_effect = [["1.3.6.1.2.1.1.2.1.3.6.1.4.1.4"], ["2"], ["3"], ["4"],
                                                             ["5"], ["6"]]
        snmp_service_mock.return_value.__enter__.return_value = snmp_recorder_mock

        # Act
        result = snmp_orchestrator.create_recording()

        # Assert
        self.assertEqual(result, response_list)

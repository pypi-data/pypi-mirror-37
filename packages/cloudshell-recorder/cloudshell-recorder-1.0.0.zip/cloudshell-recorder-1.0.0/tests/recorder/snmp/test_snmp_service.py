from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.snmp.snmp_service import SnmpService


class TestSnmpService(TestCase):

    @patch("cloudshell.recorder.snmp.snmp_service.SnmpRecorder")
    def test_get_recorder(self, snmp_recorder_mock):
        # Setup
        params = MagicMock()

        # Act
        snmp_service = SnmpService(params)
        with snmp_service as recorder:
            recorder.create_snmp_record()

        # Assert
        self.assertEqual(params, snmp_service._snmp_parameters)
        snmp_recorder_mock.assert_called_once_with(params)
        params.close_snmp_engine_dispatcher.assert_called_once()

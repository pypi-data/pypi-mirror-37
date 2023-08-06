from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.snmp.snmp_recorder import SnmpRecorder
from snmpsim import error


# ToDo rebuild tests
class TestSnmpRecorder(TestCase):
    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"

        # Act
        result = recorder.create_snmp_record(oid)

        # Assert
        recorder._cmd_gen.sendVarBinds.assert_called_once()
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording_with_stop_oid(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"
        stop_oid = "1.1.1.1.3"

        # Act
        result = recorder.create_snmp_record(oid, stop_oid)

        # Assert
        recorder._cmd_gen.sendVarBinds.assert_called_once()
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_create_recording_entire_device(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        recorder = SnmpRecorder(params)
        oid = "1.1.1.1.1"

        # Act
        result = recorder.create_snmp_record(oid, get_subtree=False)

        # Assert
        recorder._cmd_gen.sendVarBinds.assert_called_once()
        params.snmp_engine.transportDispatcher.runDispatcher.assert_called_once()
        self.assertEqual(recorder._cmd_gen, cmdgen_mock.BulkCommandGenerator.return_value)

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    @patch("cloudshell.recorder.snmp.snmp_recorder.SnmpRecord")
    def test_cb_fun(self, snmp_record, log_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        snmp_engine = MagicMock()
        send_request_handle = MagicMock()
        error_indication = None
        error_status = None
        error_index = None
        var_bind_table = [(("1", MagicMock(return_value="9")), ("5", MagicMock(return_value="9"))),
                          (("2", MagicMock(return_value="9")), ("4", MagicMock(return_value="9")))]
        cb_ctx = MagicMock()
        recorder = SnmpRecorder(params)
        recorder._cmd_gen = MagicMock()
        snmp_record.return_value.format.side_effect = ["0", error.MoreDataNotification, "0", "0", "0"]

        # Act
        recorder.cb_fun(snmp_engine, send_request_handle, error_indication,
                        error_status, error_index, var_bind_table, cb_ctx)

        # Assert
        recorder._cmd_gen.sendVarBinds.assert_called_with(snmp_engine,
                                                          'tgt',
                                                          params.v3_context_engine_id, params.v3_context,
                                                          0, params.get_bulk_repetitions,
                                                          [(None, None)],
                                                          recorder.cb_fun, cb_ctx)
        self.assertEqual(1, recorder._cmd_gen.sendVarBinds.call_count)

    @patch("cloudshell.recorder.snmp.snmp_recorder.udp6")
    @patch("cloudshell.recorder.snmp.snmp_recorder.cmdgen")
    @patch("cloudshell.recorder.snmp.snmp_recorder.error")
    @patch("cloudshell.recorder.snmp.snmp_recorder.log")
    def test_cb_fun_with_error_status(self, log_mock, error_mock, cmdgen_mock, udp6):
        # Setup
        params = MagicMock()
        snmp_engine = MagicMock()
        send_request_handle = MagicMock()
        error_indication = None
        error_status = MagicMock(return_value=1)
        error_index = None
        var_bind_table = MagicMock(side_effect={"1": "2", "2": "3"})
        cb_ctx = MagicMock(return_value={"retries": "90"})
        recorder = SnmpRecorder(params)
        recorder._cmd_gen = MagicMock()

        # Act
        recorder.cb_fun(snmp_engine, send_request_handle, error_indication,
                        error_status, error_index, var_bind_table, cb_ctx)

        # Assert
        recorder._cmd_gen.sendVarBinds.assert_called_with(snmp_engine,
                                                          'tgt',
                                                          params.v3_context_engine_id, params.v3_context,
                                                          0, params.get_bulk_repetitions,
                                                          [(
                                                           var_bind_table.__getitem__.return_value.__getitem__.return_value.__getitem__.return_value,
                                                           None)],
                                                          recorder.cb_fun, cb_ctx)
        self.assertEqual(1, recorder._cmd_gen.sendVarBinds.call_count)

from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.model.snmp_record import SnmpRecord


class TestSnmpRecord(TestCase):

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_string(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "4"
        value = "test"
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "OctetString", "0x" + value.encode("hex")), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_hex_string(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "4x"
        value = "0xtest"
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "OctetString", value), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_int(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "2"
        value = "0"
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "Integer", value), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_ip(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "64"
        value = "1.1.1.1"
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)
        socket_mock.inet_ntoa.return_value = value

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "IpAddress", value), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)
        socket_mock.inet_ntoa.assert_called_with(value)

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_time_tick(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "67"
        value = "4984654"
        time_tick_value = "13 hours, 50 minutes, 46 seconds."
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)
        socket_mock.inet_ntoa.return_value = value

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "TimeTicks", time_tick_value), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)

    @patch("cloudshell.recorder.model.snmp_record.SnmprecRecord")
    @patch("cloudshell.recorder.model.snmp_record.NoDataNotification")
    @patch("cloudshell.recorder.model.snmp_record.socket")
    def test_formatValue_0_time_tick(self, socket_mock, no_data_mock, snmrec_mock):
        # Setup
        oid = "1.1.1.11.1"
        type = "67"
        value = "0"
        time_tick_value = "0 hours, 0 minutes, 0 seconds."
        record = SnmpRecord()
        snmrec_mock.formatValue.return_value = (oid, type, value)
        socket_mock.inet_ntoa.return_value = value

        # Act
        result = record.formatValue(oid, value, context=MagicMock())

        # Assert
        self.assertEqual((oid, "TimeTicks", time_tick_value), result)
        snmrec_mock.formatValue.assert_called_once_with(record, oid, value)
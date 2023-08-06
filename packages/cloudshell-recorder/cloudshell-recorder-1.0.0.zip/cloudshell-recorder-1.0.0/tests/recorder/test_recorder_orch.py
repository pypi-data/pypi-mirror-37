from unittest import TestCase

from mock import patch, MagicMock

from cloudshell.recorder.recorder_orchestrator import RecorderOrchestrator


class TestRecorderOrchestrator(TestCase):
    IP = "1.1.1.1"
    PORT = 161
    DST_PATH = ".\\"
    REC_SNMP = "snmp"
    REC_All = "all"
    REC_CLI = "cli"
    REC_API = "api"

    def get_recorder(self, recording_type="snmp"):
        return RecorderOrchestrator(ip=self.IP, recording_type=recording_type, destination_path=self.DST_PATH)

    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_snmp_recording", return_value="")
    def test_new_recording_basic_snmp(self, snmp_mock):
        # Setup
        recorder = self.get_recorder(self.REC_SNMP)
        snmp_community = "test_public"

        # Act
        recorder.new_recording(snmp_community=snmp_community)

        # Assert
        snmp_mock.assert_called_once_with(snmp_auth_protocol=None, snmp_auto_detect_vendor=False, snmp_bulk=False,
                                          snmp_bulk_repetitions=25, snmp_community=snmp_community, snmp_password=None,
                                          snmp_priv_protocol=None, snmp_private_key=None, snmp_record=None,
                                          snmp_retries=2, snmp_timeout=2000, snmp_user=None)

    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_cli_recording", return_value=[""])
    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_snmp_recording", return_value=[""])
    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_rest_recording", return_value=[""])
    @patch("cloudshell.recorder.recorder_orchestrator.create_output_archive", return_value="")
    def test_new_recording_basic(self, zip_mock, rest_mock, snmp_mock, cli_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        user = "user"
        password = "password"
        en_password = "enable password"
        snmp_community = "test_public"

        # Act
        recorder.new_recording(cli_user=user, cli_password=password, cli_enable_password=en_password, rest_user=user,
                               rest_password=password,
                               snmp_community=snmp_community)

        # Assert
        snmp_mock.assert_called_once_with(snmp_auth_protocol=None, snmp_auto_detect_vendor=False, snmp_bulk=False,
                                          snmp_bulk_repetitions=25, snmp_community=snmp_community, snmp_password=None,
                                          snmp_priv_protocol=None, snmp_private_key=None, snmp_record=None,
                                          snmp_retries=2, snmp_timeout=2000, snmp_user=None)
        cli_mock.assert_called_once_with(cli_user=user, cli_password=password,
                                         cli_enable_password=en_password, cli_session_type="auto")

        rest_mock.assert_called_once_with(rest_user=user, rest_password=password,
                                          rest_token=None)
        zip_mock.assert_called_once_with(snmp_mock.return_value, cli_mock.return_value, rest_mock.return_value,
                                         self.DST_PATH, self.IP)

    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_cli_recording", return_value="")
    def test_new_recording_basic_cli(self, cli_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        user = "user"
        password = "password"
        en_password = "enable password"
        connection_type = "ssh"

        # Act
        recorder.new_recording(cli_user=user, cli_password=password, cli_enable_password=en_password,
                               cli_session_type=connection_type)

        # Assert
        cli_mock.assert_called_once_with(cli_user=user, cli_password=password,
                                         cli_enable_password=en_password,
                                         cli_session_type=connection_type)

    @patch("cloudshell.recorder.recorder_orchestrator.RecorderOrchestrator._new_rest_recording", return_value="")
    def test_new_recording_basic_rest(self, rest_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        user = "user"
        password = "password"

        # Act
        recorder.new_recording(rest_user=user, rest_password=password)

        # Assert
        rest_mock.assert_called_once_with(rest_user=user, rest_password=password,
                                          rest_token=None)

    @patch("cloudshell.recorder.recorder_orchestrator.SNMPOrchestrator")
    @patch("cloudshell.recorder.recorder_orchestrator.SnmpV2Parameters")
    @patch("cloudshell.recorder.recorder_orchestrator.ENTIRE_SNMP_OID_LIST")
    def test_snmp_v2_recording(self, oids_list_mock, snmp_v2_params, snmp_orch_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        snmp_community = "test_public"
        create_recording_mock = MagicMock()
        snmp_orch_mock.return_value.create_recording = create_recording_mock

        # Act
        recorder._new_snmp_recording(snmp_community=snmp_community, snmp_record="all")

        # Assert
        snmp_v2_params.assert_called_once_with(self.IP,
                                               snmp_community=snmp_community,
                                               is_ipv6=False,
                                               port=self.PORT,
                                               timeout=2000,
                                               retry_count=2,
                                               get_bulk_flag=False,
                                               get_bulk_repetitions=25,
                                               continue_on_errors=0,
                                               v3_context_engine_id=None,
                                               v3_context='')
        snmp_orch_mock.assert_called_once_with(snmp_v2_params.return_value,
                                               auto_detect_vendor=False,
                                               template_oid_list=oids_list_mock)
        create_recording_mock.assert_called_once()

    @patch("cloudshell.recorder.recorder_orchestrator.SNMPOrchestrator")
    @patch("cloudshell.recorder.recorder_orchestrator.SnmpV2Parameters")
    @patch("cloudshell.recorder.recorder_orchestrator.open", create=True, return_value=MagicMock(spec=file))
    def test_snmp_v2_recording_custom_oids(self, open_mock, snmp_v2_params, snmp_orch_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        snmp_community = "test_public"
        oids_list = ["test", "test"]
        create_recording_mock = MagicMock()
        snmp_orch_mock.return_value.create_recording = create_recording_mock
        open_mock.return_value.__enter__.return_value.read.return_value.split.return_value = oids_list

        # Act
        recorder._new_snmp_recording(snmp_community=snmp_community, snmp_record="template:.\\path_to_file")

        # Assert
        snmp_v2_params.assert_called_once_with(self.IP,
                                               snmp_community=snmp_community,
                                               is_ipv6=False,
                                               port=self.PORT,
                                               timeout=2000,
                                               retry_count=2,
                                               get_bulk_flag=False,
                                               get_bulk_repetitions=25,
                                               continue_on_errors=0,
                                               v3_context_engine_id=None,
                                               v3_context='')
        snmp_orch_mock.assert_called_once_with(snmp_v2_params.return_value,
                                               auto_detect_vendor=False,
                                               template_oid_list=oids_list)
        create_recording_mock.assert_called_once()

    @patch("cloudshell.recorder.recorder_orchestrator.SNMPOrchestrator")
    @patch("cloudshell.recorder.recorder_orchestrator.SnmpV3Parameters")
    @patch("cloudshell.recorder.recorder_orchestrator.DEFAULT_SNMP_OID_LIST")
    def test_snmp_v3_recording(self, oids_list_mock, snmp_v3_params, snmp_orch_mock):
        # Setup
        recorder = self.get_recorder(self.REC_All)
        snmp_user = "user"
        snmp_password = "password"
        snmp_private_key = "priv_key"
        snmp_auth_protocol = "SHA"
        snmp_priv_protocol = "DES"
        create_recording_mock = MagicMock()
        snmp_orch_mock.return_value.create_recording = create_recording_mock

        # Act
        recorder._new_snmp_recording(snmp_user=snmp_user, snmp_password=snmp_password,
                                     snmp_private_key=snmp_private_key, snmp_auth_protocol=snmp_auth_protocol,
                                     snmp_priv_protocol=snmp_priv_protocol)

        # Assert
        snmp_v3_params.assert_called_once_with(self.IP, v3_user=snmp_user, v3_auth_key=snmp_password,
                                               v3_priv_key=snmp_private_key,
                                               v3_auth_proto=snmp_auth_protocol,
                                               v3_priv_proto=snmp_priv_protocol, port=self.PORT,
                                               is_ipv6=False, timeout=2000,
                                               retry_count=2, get_bulk_flag=False,
                                               continue_on_errors=0,
                                               get_bulk_repetitions=25,
                                               v3_context_engine_id=None,
                                               v3_context="")
        snmp_orch_mock.assert_called_once_with(snmp_v3_params.return_value,
                                               auto_detect_vendor=False,
                                               template_oid_list=oids_list_mock)
        create_recording_mock.assert_called_once()

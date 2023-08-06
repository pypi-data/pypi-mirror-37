from unittest import TestCase

from mock import patch

from cloudshell.recorder.file_service.file_service import create_output_archive


class TestFilesService(TestCase):
    IP = "1.1.1.1"
    PATH = "./"

    @patch("cloudshell.recorder.file_service.file_service.ZipFile")
    @patch("cloudshell.recorder.file_service.file_service.os")
    def test_create_output_archive(self, os_mock, zip_mock):
        # Setup
        snmp_output = "1"
        snmp_name = self.IP + ".snmp"
        cli_output = "2"
        cli_name = self.IP + ".cli"
        rest_output = "3"
        rest_name = self.IP + ".rest_api"
        zip_name = self.IP + ".zip"
        zip_path = self.PATH + zip_name
        os_mock.path.join.return_value = zip_path

        # Act
        create_output_archive(cli_recording=cli_output,
                              snmp_recording=snmp_output,
                              rest_recording=rest_output,
                              path=self.PATH,
                              zip_name=self.IP)

        # Assert
        os_mock.path.join.assert_called_once_with(os_mock.path.expandvars.return_value, zip_name)
        zip_mock.assert_called_once_with(zip_path, "w")
        zip_mock.return_value.__enter__.asser_called_once()
        self.assertEqual(3, zip_mock.return_value.__enter__.return_value.writestr.call_count)
        self.assertEqual((cli_name, cli_output),
                         zip_mock.return_value.__enter__.return_value.writestr.call_args_list[0][0])
        self.assertEqual((rest_name, rest_output),
                         zip_mock.return_value.__enter__.return_value.writestr.call_args_list[1][0])
        self.assertEqual((snmp_name, snmp_output),
                         zip_mock.return_value.__enter__.return_value.writestr.call_args_list[2][0])

from unittest import TestCase

from click.testing import CliRunner
from mock import patch

from cloudshell.recorder.bootstrap import new, version


class TestBootstrap(TestCase):
    def test_new(self):
        result = CliRunner().invoke(new, ['1.1.1.1', '--snmp-community=public', '--record-type=snmp'])
        self.assertEqual(0, result.exit_code)

    @patch("cloudshell.recorder.bootstrap.pkg_resources")
    def test_version(self, pkg_mock):
        # Setup
        response = "1.0.0"
        pkg_mock.get_distribution.return_value.version = response

        # Act
        result = CliRunner().invoke(version)

        # Assert
        self.assertEqual(0, result.exit_code)
        self.assertEqual(u"cloudshell-recorder version {}\n".format(response), result.output)

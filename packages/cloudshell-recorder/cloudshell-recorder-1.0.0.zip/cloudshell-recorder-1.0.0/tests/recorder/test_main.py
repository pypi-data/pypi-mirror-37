from unittest import TestCase

from mock import patch

from cloudshell.recorder.__main__ import init


class TestMain(TestCase):
    def test_init(self):
        with patch("cloudshell.recorder.__main__.cli") as cli_mock:
            init()
            cli_mock.assert_called_once()

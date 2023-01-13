from unittest import TestCase
from mock import patch

from fall.rebooter import LinuxRebooter
from fall.fall_error import FallError

EMPTY_STRING = ''


class TestRebooter(TestCase):

    @patch('fall.utility.shell_runner.PseudoShellRunner.run', side_effect=[(EMPTY_STRING, EMPTY_STRING, -1)])
    def test_non_docker_reboot_linux_fail(self, mock_runner):
        with self.assertRaisesRegex(FallError, "Firmware Update Aborted: Reboot Failed: "):
            LinuxRebooter().reboot()

    @patch('fall.utility.shell_runner.PseudoShellRunner.run', side_effect=[(EMPTY_STRING, EMPTY_STRING, 0)])
    def test_non_docker_reboot_linux_pass(self, mock_runner):
        try:
            LinuxRebooter().reboot()
        except FallError:
            self.fail("FallError received when not expected")

    @patch('os.environ.get', return_value=True)
    @patch('fall.utility.shell_runner.PseudoShellRunner.run', side_effect=[(EMPTY_STRING, EMPTY_STRING, 0)])
    def test_reboot_docker_app_linux_pass(self, mock_runner, mock_is_docker):
        try:
            LinuxRebooter().reboot()
        except FallError:
            self.fail("FallError received when not expected")

from unittest import TestCase
from fall.utility.shell_runner import PseudoShellRunner
from mock import mock_open, patch
import mock


class TestShellRunner(TestCase):

    class MockPopen:

        def __init__(self):
            pass

        def communicate(self, input=None):
            return 'stdout', 'stderr'

        def close(self):
            pass

    # @patch('os.makedirs', return_value=True)
    # def test_run_file(self, mock_makedir):
    #     with patch('builtins.open', new_callable=mock_open()) as m:
    #         mock_popen = TestShellRunner.MockPopen()
    #         mock_returncode = mock.PropertyMock(return_value=0)
    #         type(mock_popen).returncode = mock_returncode  # type: ignore
    #
    #         out, err, return_cod = PseudoShellRunner.run_with_log_path(
    #             "echo TestCase", "/home/fakepath/")
    #         mock_makedir.assert_called_once()
    #         self.assertEquals(out, '')

    @patch('os.makedirs', return_value=True)
    def test_run_stdout(self, mock_makedir):
        with patch('builtins.open', new_callable=mock_open()):
            mock_popen = TestShellRunner.MockPopen()
            mock_makedir.assert_not_called()
            mock_returncode = mock.PropertyMock(return_value=0)
            type(mock_popen).return_code = mock_returncode  # type: ignore

            out, err, return_code = PseudoShellRunner.run("echo TestCase")
            self.assertEqual(out, "TestCase\n")

    def test_sanitize(self, filename='test file/name'):
        self.assertEqual(
            PseudoShellRunner._sanitize(filename),
            'test_file_name')

from unittest import TestCase
from mock import patch

from fall.host_os import OsType, get_host_os


class TestHostOs(TestCase):
    @patch('fall.host_os.platform.system', return_value='Linux')
    @patch('os.environ.get', return_value=False)
    def test_get_linux_os_outside_container(self, mock_is_container, mock_platform):
        self.assertEqual(get_host_os(), OsType.Linux)

    @patch('os.environ.get', return_value=True)
    def test_get_linux_os_inside_container(self, mock_is_container):
        self.assertEqual(get_host_os(), OsType.Linux)

    @patch('fall.host_os.platform.system', return_value='Windows')
    @patch('os.environ.get', return_value=False)
    def test_raise_value_error_unsupported_os(self, mock_is_container, mock_platform):
        with self.assertRaisesRegex(ValueError, 'Unsupported OS Type'):
            get_host_os()

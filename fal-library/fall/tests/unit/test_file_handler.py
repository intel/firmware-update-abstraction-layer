import builtins

from unittest import TestCase

from fall.utility.file_handler import get_canonical_representation_of_path, read_file, is_path_exist, move_file
from mock import patch, mock_open


class TestUtility(TestCase):
    def test_get_canonical_representation_of_absolute_path(self):
        self.assertEqual('/var/cache/manageability',
                         get_canonical_representation_of_path("/var/cache/manageability"))

    @patch.object(builtins, "open", new_callable=mock_open, read_data="Intel")
    @patch('fall.utility.file_handler.os.path.exists', return_value=True)
    def test_read_vendor_successfully(self, mock_exists, mock_readline):
        value = read_file('/sys/devices/virtual/dmi/bios_vendor', 'UNKNOWN')
        self.assertEqual(value, 'Intel')

    @patch('fall.utility.file_handler.os.path.exists', return_value=False)
    def test_unable_to_read_vendor(self, mock_exists):
        value = read_file('/sys/devices/virtual/dmi/bios_vendor', 'UNKNOWN')
        self.assertEqual(value, 'UNKNOWN')

    @patch('fall.utility.file_handler.open', side_effect=OSError('No Privileges'))
    @patch('fall.utility.file_handler.os.path.exists', return_value=True)
    def test_raise_while_read_line(self, mock_exists, mock_file):
        with self.assertRaisesRegex(ValueError,
                                    'No Privileges Error while reading the file /sys/devices/virtual/dmi/bios_vendor'):
            read_file('/sys/devices/virtual/dmi/bios_vendor', 'UNKNOWN')

    @patch('fall.utility.file_handler.os.path.isdir', return_value=True)
    def test_dmi_path_exists(self, mock_isdir):
        self.assertTrue(is_path_exist('/sys/devices/virtual/dmi/'))

    @patch('fall.utility.file_handler.os.path.isdir', return_value=False)
    def test_dmi_path_does_not_exist(self, mock_isdir):
        self.assertFalse(is_path_exist('/sys/devices/virtual/dmi/'))

    @patch('shutil.move')
    @patch('os.path.exists', return_value=True)
    def test_move_file_successfully(self, os_path, move_file):
        try:
            move_file('/home/usr', '/etc')
        except IOError as e:
            self.fail(f"Unexpected exception raised during test: {e}")
        # os_path.assert_called_once()
        # move_file.assert_called()

    @patch('os.path.exists', return_value=False)
    def test_raise_when_move_file_dne(self, os_path):
        with self.assertRaises(IOError):
            move_file('/home/usr', '/etc')
        # os_path.assert_called_once()
        # move_file.assert_not_called()

    @patch('os.path.exists', return_value=True)
    def test_move_file_throw_exception(self, os_path):
        with self.assertRaises(IOError):
            move_file('/home/usr', '/etc')
        # os_path.assert_called_once()

    @patch("os.path.islink", return_value=True)
    def test_raises_when_move_src_is_symlink(self, mock_is_symlink):
        with self.assertRaises(IOError):
            move_file('/home/usr', '/etc')

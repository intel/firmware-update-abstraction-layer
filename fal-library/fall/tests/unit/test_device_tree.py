import datetime

from unittest import TestCase
from mock import patch
from fall.device_tree import get_device_tree_system_info, _parse_bios_date
from fall.utility.file_handler import is_path_exist


class TestDeviceTree(TestCase):

    @patch('fall.device_tree._parse_bios_date', return_value='1/15/2022')
    def test_get_device_tree_system_info(self, mock_date):
        if is_path_exist('/proc/device-tree/'):
            actual = get_device_tree_system_info()
            expected = devicetree_parsed_1
            self.assertEqual(actual, expected)

    def test_parse_correct_release_date_format(self):
        self.assertEqual(_parse_bios_date('Jun 27 2019 16:04:32'), devicetree_date)

    def test_raise_invalid_date_format(self):
        with self.assertRaisesRegex(ValueError, 'Time date \'2019-06-30 16:04:32\' does not match expected format'):
            _parse_bios_date('2019-06-30 16:04:32')


devicetree_date = '2019-06-27'

devicetree_system_info = ''

DEVICE_TREE_PATH = '/proc/device-tree/'

devicetree_parsed_1 = (datetime.datetime(2006, 12, 1, 0, 0),
                       'innotek GmbH',
                       'VirtualBox',
                       'innotek GmbH',
                       'VirtualBox',
                       True)

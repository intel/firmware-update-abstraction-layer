from unittest import TestCase
from fall.platform_finder import LinuxPlatformFinder
from fall.platform_info import PlatformInformation
from mock import patch


class TestPlatformFinder(TestCase):

    platform_info = PlatformInformation()

    @patch('fall.platform_finder.get_dmi_system_info',
           return_value=PlatformInformation('1/15/2022', 'Intel Corp.', 'BNKBL357.86A.0042.2017.0303.1854', '', ''))
    @patch('fall.platform_finder.is_path_exist', return_value=True)
    def test_get_linux_info_dmi(self, mock_exist, mock_dmi):
        LinuxPlatformFinder().get()
        mock_dmi.assert_called_once()

    @patch('fall.platform_finder.get_device_tree_system_info')
    @patch('fall.platform_finder.is_path_exist', return_value=False)
    def test_get_linux_info_device_tree(self, mock_exist, mock_device_tree):
        LinuxPlatformFinder().get()
        mock_device_tree.assert_called_once()

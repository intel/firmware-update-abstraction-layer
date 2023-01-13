import builtins

from unittest import TestCase
from mock import patch, mock_open

from fall.platform_info import PlatformInformation
from fall.dmi import get_dmi_system_info, _parse_release_date


class TestDmi(TestCase):

    @patch('fall.dmi.read_file')
    def test_get_dmi_info(self, mock_read):
        mock_read.side_effect = ['1/15/2022', 'Intel',
                                 'BNKBL357.86A.0042.2017.0303', 'Intel Corp.', 'KMB']
        expected = PlatformInformation(bios_release_date='2022-01-15', bios_vendor='Intel',
                                       bios_version='BNKBL357.86A.0042.2017.0303', platform_mfg='Intel Corp.',
                                       platform_name='KMB')

        self.assertEqual(get_dmi_system_info(), expected)

    @patch.object(builtins, "open", new_callable=mock_open, read_data="Unknown")
    @patch('fall.dmi._parse_release_date', return_value='1/15/2022')
    def test_unknown_dmi_info(self, mock_date, mock_read):
        expected = PlatformInformation('Unknown', 'Unknown', 'Unknown', '', '')
        self.assertEqual(get_dmi_system_info(), expected)

    def test_parse_release_date(self):
        self.assertEqual(_parse_release_date('10/15/2018'), '2018-10-15')

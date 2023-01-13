import os
from unittest import TestCase

from fall.configuration_finder import ConfigurationFinder
from fall.platform_info import PlatformInformation
from fall.fall_error import FallError

TEST_SCHEMA_LOCATION = os.path.join(os.path.dirname(__file__),
                                    '../../schema/firmware_schema.xsd')

TEST_XML_FILE = os.path.join(os.path.dirname(__file__),
                             '../../db/firmware_info.db')

GOOD_XML = '<?xml version="1.0" encoding="utf-8"?><firmware_component>' \
           '<firmware_product name=\'NUC6CAYS\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>UpdateBIOS.sh</firmware_tool><firmware_file_type>bio</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'Broxton P\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_dest_path>/boot/efi/</firmware_dest_path><firmware_file_type>xx</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'Default string\'><bios_vendor>American Megatrends Inc.</bios_vendor><operating_system>linux</operating_system><tool_options>/p /b</tool_options><firmware_tool>/opt/afulnx/afulnx_64</firmware_tool><firmware_file_type>xx</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'kmb-evm\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>/usr/sbin/movisoc-fwu</firmware_tool><firmware_tool_args>-a</firmware_tool_args><firmware_file_type>xx</firmware_file_type><firmware_tool_check_args>--usage</firmware_tool_check_args></firmware_product>' \
           '<firmware_product name=\'Alder Lake Client Platform\' guid=\'true\'><bios_vendor>Intel Corporation</bios_vendor><operating_system>linux</operating_system><firmware_tool>fwupdate</firmware_tool><firmware_tool_args>--apply</firmware_tool_args><firmware_tool_check_args>-s</firmware_tool_check_args><firmware_file_type>xx</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'NUC7i5DNKPC\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>windows</operating_system><firmware_file_type>msi</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'kmb-hddl2\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>/usr/sbin/movisoc-fwu</firmware_tool><firmware_tool_args>-a</firmware_tool_args><firmware_file_type>xx</firmware_file_type><firmware_tool_check_args>--usage</firmware_tool_check_args></firmware_product>' \
           '<firmware_product name=\'EMBC5000\' tool_options=\'true\'><bios_vendor>American Megatrends International, LLC.</bios_vendor><operating_system>linux</operating_system><firmware_tool>afulnx_64</firmware_tool><firmware_file_type>xx</firmware_file_type></firmware_product></firmware_component>'


class TestConfigurationFinder(TestCase):

    def setUp(self):
        platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel',
                                            bios_version='4.0', platform_mfg='Intel Corp', platform_name='kmb-evm')
        self.config_finder = ConfigurationFinder(
            platform_info, xml=TEST_XML_FILE, schema=TEST_SCHEMA_LOCATION)

    def test_find_match(self):
        update_info = self.config_finder.find_match()
        self.assertEqual(update_info.tool_path, '/usr/sbin/movisoc-fwu')

    def test_raise_platform_dne(self):
        platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel',
                                            bios_version='4.0', platform_mfg='Intel Corp', platform_name='kmb')
        dne_finder = ConfigurationFinder(
            platform_info, xml=TEST_XML_FILE, schema=TEST_SCHEMA_LOCATION)
        with self.assertRaisesRegex(FallError, 'The platform is unsupported - kmb'):
            dne_finder.find_match()

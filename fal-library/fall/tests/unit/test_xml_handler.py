import os
from unittest import TestCase

from fall.xml_handler import XmlHandler, XmlException

TEST_SCHEMA_LOCATION = os.path.join(os.path.dirname(__file__),
                                    '../../schema/firmware_schema.xsd')

BAD_SCHEMA_LOCATION = os.path.join(os.path.dirname(__file__),
                                   '../../../schema/fw_schema.xsd')

GOOD_XML = '<?xml version="1.0" encoding="utf-8"?><firmware_component>' \
           '<firmware_product name=\'NUC6CAYS\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>UpdateBIOS.sh</firmware_tool><firmware_file_type>bio</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'Broxton P\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_dest_path>/boot/efi/</firmware_dest_path><firmware_file_type>xx</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'Default string\'><bios_vendor>American Megatrends Inc.</bios_vendor><operating_system>linux</operating_system><firmware_tool>/opt/afulnx/afulnx_64</firmware_tool><firmware_file_type>xx</firmware_file_type><tool_options>/p /b</tool_options></firmware_product>' \
           '<firmware_product name=\'kmb-evm\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>/usr/sbin/movisoc-fwu</firmware_tool><firmware_tool_args>-a</firmware_tool_args><firmware_file_type>xx</firmware_file_type><firmware_tool_check_args>--usage</firmware_tool_check_args></firmware_product>' \
           '<firmware_product name=\'Alder Lake Client Platform\' guid=\'true\'><bios_vendor>Intel Corporation</bios_vendor><operating_system>linux</operating_system><firmware_tool>fwupdate</firmware_tool><firmware_tool_args>--apply</firmware_tool_args><firmware_tool_check_args>-s</firmware_tool_check_args><firmware_file_type>xx</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'NUC7i5DNKPC\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>windows</operating_system><firmware_file_type>msi</firmware_file_type></firmware_product>' \
           '<firmware_product name=\'kmb-hddl2\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>/usr/sbin/movisoc-fwu</firmware_tool><firmware_tool_args>-a</firmware_tool_args><firmware_file_type>xx</firmware_file_type><firmware_tool_check_args>--usage</firmware_tool_check_args></firmware_product>' \
           '<firmware_product name=\'EMBC5000\'><bios_vendor>American Megatrends International, LLC.</bios_vendor><operating_system>linux</operating_system><firmware_tool>afulnx_64</firmware_tool><firmware_file_type>xx</firmware_file_type><tool_options>/p /b</tool_options></firmware_product></firmware_component>'

BAD_XML = '<?xml version="1.0" encoding="utf-8"?><firmware_component>' \
          '<firmware_product name=\'NUC6CAYS\'><bios_vendor>Intel Corp.</bios_vendor><operating_system>linux</operating_system><firmware_tool>UpdateBIOS.sh</firmware_tool><firmware_file_type>bio<firmware_file_type></firmware_product>></firmware_component>'

EMPTY_TAG_XML = '<?xml version="1.0" encoding="utf-8"?><firmware_component>' \
                '<firmware_product name=\'NUC6CAYS\'><bios_vendor>Intel Corp.</bios_vendor><operating_system></operating_system><firmware_tool>UpdateBIOS.sh</firmware_tool><firmware_file_type>bio<firmware_file_type></firmware_product>></firmware_component>'


class TestXmlHandler(TestCase):

    def setUp(self) -> None:
        self.good = XmlHandler(GOOD_XML, is_file=False, schema_location=TEST_SCHEMA_LOCATION)

    def test_parser_creation_success(self) -> None:
        self.assertIsNotNone(self.good)

    def test_parser_creation_failure(self) -> None:
        with self.assertRaises(XmlException):
            XmlHandler(xml=BAD_XML, is_file=False, schema_location=TEST_SCHEMA_LOCATION)

    def test_get_all_platform(self):
        try:
            platforms = self.good.get_root_elements('firmware_product', 'name')
            self.assertEqual(8, len(platforms))
        except XmlException:
            self.fail('Error raised unexpectedly')

    def test_raise_schema_file_not_found(self):
        with self.assertRaisesRegex(XmlException, "Error with Schema file: File does not exist or file path is not to a file."):
            XmlHandler(GOOD_XML, is_file=False, schema_location=BAD_SCHEMA_LOCATION)

    def test_get_specific_platform_by_name(self):
        try:
            child = self.good.get_children(
                f"firmware_product[@name='Alder Lake Client Platform']")
        except (XmlException, KeyError) as e:
            self.fail(f'Error raised unexpectedly: {e}')

        self.assertEqual(6, len(child))
        self.assertTrue(self.good.get_attribute(
            f"firmware_product[@name='Alder Lake Client Platform']", 'guid'))
        self.assertEqual('fwupdate', child.get('firmware_tool', None))
        self.assertEqual('Intel Corporation', child.get('bios_vendor', None))
        self.assertEqual('linux', child.get('operating_system', None))
        self.assertEqual('--apply', child.get('firmware_tool_args', None))
        self.assertEqual('-s', child.get('firmware_tool_check_args', None))

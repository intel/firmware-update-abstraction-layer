
from unittest import TestCase

from falc.parser import ArgsParser, _fw


class TestParser(TestCase):

    def setUp(self):
        self.arg_parser = ArgsParser()

    def test_fw_command_pass(self):
        f = self.arg_parser.parse_args(
            ['fw', '-p', '/var/cache/manageability/repository-tool/BIOS.img', '-d'])
        self.assertEqual(f.biosversion, '5.12')
        self.assertEqual(f.manufacturer, 'intel')
        self.assertEqual(f.path, '/var/cache/manageability/repository-tool/BIOS.img')
        self.assertEqual(f.product, 'kmb-hddl2')
        self.assertEqual(f.releasedate, '2024-12-31')
        self.assertEqual(f.vendor, 'Intel')
        self.assertEqual(f.debug, True)

    def test_query_command_pass(self):
        f = self.arg_parser.parse_args(
            ['query', '-o', 'hw'])
        self.assertEqual(f.option, 'hw')
        self.assertEqual(f.debug, False)

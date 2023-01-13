from unittest import TestCase
from falc.falc_exception import FalcException
from falc.command_factory import create_command_factory
from falc.command import FwCommand, QueryCommand


class TestOsFactory(TestCase):
    def test_create_query_command(self):
        assert type(create_command_factory("query")) is QueryCommand

    def test_create_fota_command(self):
        assert type(create_command_factory("fw")) is FwCommand

    def test_raise_on_invalid_command(self):
        with self.assertRaises(FalcException):
            create_command_factory("app")

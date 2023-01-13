from unittest import TestCase
from fall.host_os import OsType
from fall.os_factory import LinuxFactory, get_factory
from fall.platform_finder import LinuxPlatformFinder
from fall.installer import LinuxInstaller
from fall.rebooter import LinuxRebooter


class TestOsFactory(TestCase):

    def test_get_factory_linux(self):
        self.assertEqual(type(get_factory(OsType.Linux)), LinuxFactory)

    def test_create_platform_finder(self):
        self.assertEqual(type(get_factory(OsType.Linux).create_platform_finder()),
                         LinuxPlatformFinder)

    def test_create_linux_installer(self):
        self.assertEqual(type(get_factory(OsType.Linux).create_installer()), LinuxInstaller)

    def test_create_linux_rebooter(self):
        self.assertEqual(type(get_factory(OsType.Linux).create_rebooter()), LinuxRebooter)

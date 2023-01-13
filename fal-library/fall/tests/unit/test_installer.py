from unittest import TestCase

from fall.update_info import UpdateInformation
from fall.platform_info import PlatformInformation
from fall.installer import LinuxInstaller
from fall.fall_error import FallError
from mock import patch


class TestInstaller(TestCase):

    def setUp(self):
        nuc_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                bios_version='4.0', platform_mfg='Intel', platform_name='NUC7i3DNKE')
        self.nuc_update_info = UpdateInformation(platform_info=nuc_platform_info, file_type="bio",
                                                 tool_path="UpdateBIOS.sh")
        self._linux_installer = LinuxInstaller()

    @patch('fall.bios_factory.LinuxToolFirmware.install')
    def test_linux_install(self, mock_install):
        try:
            self._linux_installer.install('path/to/package', self.nuc_update_info, 384)
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")

    def test_raise_when_missing_platform_info(self):
        missing_platform_info = UpdateInformation(file_type="bio", tool_path="UpdateBIOS.sh")
        with self.assertRaisesRegex(FallError,
                                    "Platform Information unspecified"):
            self._linux_installer.install('path/to/package', missing_platform_info, 384)

    def test_raise_when_missing_platform_name(self):
        nuc_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                bios_version='4.0', platform_mfg='Intel')
        update_info = UpdateInformation(platform_info=nuc_platform_info, file_type="bio",
                                        tool_path="UpdateBIOS.sh")
        with self.assertRaisesRegex(FallError,
                                    "Platform product unspecified"):
            self._linux_installer.install('path/to/package', update_info, 384)

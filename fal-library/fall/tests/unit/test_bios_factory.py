from unittest import TestCase

import os
from fall.bios_factory import LinuxToolFirmware, LinuxFileFirmware, BiosFactory
from fall.fall_error import FallError
from fall.update_info import UpdateInformation
from fall.platform_info import PlatformInformation
from fall.packagemanager.local_repo import DirectoryRepo
from mock import patch

FILE_CERT = 'file.cert'
FILE_FAKE = 'file.fake'
FILE_FV = 'file.fv'
FILE_BIN = 'file.bin'
PSEUDO_RUN = 'fall.utility.shell_runner.PseudoShellRunner.run'
BLANK_STRING = ''


class TestBiosFactory(TestCase):

    def setUp(self):
        kmb_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                bios_version='3', platform_mfg='Intel', platform_name='kmb-evm')
        self.kmb_update_info = UpdateInformation(platform_info=kmb_platform_info, file_type='xx', tool_args='-a',
                                                 tool_path='/usr/sbin/movisoc-fwu', firmware_tool_check_args='--usage')

        apl_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                bios_version='4.0', platform_mfg='Intel', platform_name='Broxton P')
        self.apl_update_info = UpdateInformation(platform_info=apl_platform_info, file_type="xx",
                                                 firmware_destination='/boot/efi/')

        nuc_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                bios_version='4.0', platform_mfg='Intel', platform_name='NUC7i3DNKE')
        self.nuc_update_info = UpdateInformation(platform_info=nuc_platform_info, file_type="bio",
                                                 tool_path="UpdateBIOS.sh")

        lake_platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel Corp.',
                                                 bios_version='4.0', platform_mfg='Intel',
                                                 platform_name='Tiger Lake Client Platform')
        self.lake_update_info = UpdateInformation(platform_info=lake_platform_info, is_guid_required=True,
                                                  firmware_tool_check_args='-s', tool_path='fwupdate',
                                                  file_type='xx', tool_args='--apply')

        self.repo = DirectoryRepo(os.path.dirname('/path/to/package'))

    def test_get_factory_linux_tool_type(self):
        self.assertEqual(type(BiosFactory.get_factory(
            self.repo, self.nuc_update_info)), LinuxToolFirmware)

    def test_get_factory_linux_file_type(self):
        self.assertEqual(type(BiosFactory.get_factory(
            self.repo, self.apl_update_info)), LinuxFileFirmware)

    @patch('fall.bios_factory.move_file')
    def test_install_linux_file_firmware_successfully(self, mock_move):
        try:
            LinuxFileFirmware(self.repo, self.apl_update_info).install('package_name')
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")
        mock_move.assert_called_once()

    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, BLANK_STRING, 0))
    @patch('os.path.isfile', return_value=True)
    def test_install_linux_tool_firmware_successfully(self, mock_is_file, mock_runner):
        try:
            LinuxToolFirmware(self.repo, self.apl_update_info).install('package_name')
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")
        mock_runner.assert_called_once()

    @patch('fall.bios_factory.LinuxToolFirmware._apply_firmware', side_effect=ValueError)
    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, BLANK_STRING, 0))
    @patch('os.path.isfile', return_value=True)
    def test_install_raises_value_error_applying_fw(self, mock_is_file, mock_runner, mock_apply_fw):
        with self.assertRaises(FallError):
            LinuxToolFirmware(self.repo, self.apl_update_info).install('package_name')

    @patch('fall.bios_factory.move_file', side_effect=IOError("Error while moving file: file.bin"))
    def test_raise_error_moving_file_on_install(self, mock_move):
        with self.assertRaises(FallError):
            LinuxFileFirmware(self.repo, self.apl_update_info).install('package_name')

    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, BLANK_STRING, 0))
    @patch('os.environ.get', return_value=True)
    def test_apply_firmware_docker_container(self, mock_environ, mock_runner):
        try:
            LinuxToolFirmware(self.repo, self.kmb_update_info)._apply_firmware('file')
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")

    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, BLANK_STRING, 0))
    @patch('os.environ.get', return_value=False)
    def test_apply_firmware_native(self, mock_environ, mock_runner):
        try:
            LinuxToolFirmware(self.repo, self.kmb_update_info)._apply_firmware('file')
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")

    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, 'some err', 5))
    @patch('os.environ.get', return_value=True)
    def test_raise_failed_command_apply_firmware_docker_container(self, mock_environ, mock_runner):
        with self.assertRaisesRegex(FallError, 'some err'):
            LinuxToolFirmware(self.repo, self.kmb_update_info)._apply_firmware('filename')

    @patch(PSEUDO_RUN, return_value=(BLANK_STRING, '', 5))
    @patch('os.environ.get', return_value=True)
    def test_raise_generic_err_str_when_failed_command_apply_firmware_docker_container(self, mock_environ, mock_runner):
        with self.assertRaisesRegex(FallError, 'Firmware command failed'):
            LinuxToolFirmware(self.repo, self.kmb_update_info)._apply_firmware('filename')

    @patch('fall.bios_factory.os.path.isfile', return_value=False)
    def test_raise_tool_not_found_kmb(self, mock_isfile):
        with self.assertRaisesRegex(FallError,
                                    "Firmware Update Aborted:  Firmware tool does not exist at /usr/sbin/movisoc-fwu"):
            LinuxToolFirmware(self.repo, self.kmb_update_info).install('package_name')

    @patch(PSEUDO_RUN, return_value=('cert', 'some error', 127))
    @patch('fall.bios_factory.os.path.isfile', return_value=True)
    def test_raise_tool_failure(self, mock_isfile, mock_runner):
        with self.assertRaisesRegex(FallError,
                                    "Firmware Update Aborted: Firmware tool: some err"):
            LinuxToolFirmware(self.repo, self.kmb_update_info).install('package_name')
        mock_runner.assert_called_once()

    @patch(PSEUDO_RUN,
           return_value=('system-firmware type, {21c06e7c-bd27-8462-0238-61c13de6162c} version 42 can be updated to any version above 41', BLANK_STRING, 0))
    def test_extract_guid(self, mock_guid):
        try:
            guid = LinuxToolFirmware(self.repo, self.lake_update_info)._extract_guid()
            self.assertEqual(guid, '21c06e7c-bd27-8462-0238-61c13de6162c')
        except FallError as e:
            self.fail(f"raised unexpectedly! --> {e}")

    @patch(PSEUDO_RUN,
           return_value=('fwupdate is not recognized as an internal or external command.', 'some err', 35))
    def test_raise_get_guid_fails(self, mock_guid):
        with self.assertRaisesRegex(FallError,
                                    "Firmware Update Aborted: failed to list GUIDs: some err"):
            LinuxToolFirmware(self.repo, self.lake_update_info)._extract_guid()

    @patch(PSEUDO_RUN,
           return_value=(
               ' {21c06e7c-bd27-8462-0238-61c13de6162c} version 42 can be updated to any version above 41',
               BLANK_STRING, 0))
    def test_raise_no_guid_when_required(self, mock_guid):
        with self.assertRaisesRegex(FallError,
                                    "Firmware Update Aborted: No System Firmware type GUID found"):
            LinuxToolFirmware(self.repo, self.lake_update_info)._extract_guid()

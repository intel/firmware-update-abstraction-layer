from unittest import TestCase
from mock import patch

from fall.firmware_updater import FirmwareUpdater
from fall.update_info import UpdateInformation
from fall.platform_info import PlatformInformation
from fall.fall_error import FallError
from fall.host_os import OsType
from fall.result_constants import INSTALL_SUCCESS, INPUT_VALIDATION_FAILURE, UNSUPPORTED_OS_FAILURE, \
    UNABLE_TO_GET_PLATFORM_INFO_FAILURE, UPGRADE_CHECK_FAILURE, INSTALL_FAILURE, UNABLE_FIND_MATCHING_PLATFORM, Result

BIOS_LOCATION = '/var/cache/manageability/bios.bin'
RELEASE_DATE = '2022-12-12'
INTEL = 'Intel'
VALID_PATH = 'fall.firmware_updater.is_valid_path'


class TestFirmwareUpdater(TestCase):

    def setUp(self):
        self.fw_updater = FirmwareUpdater()
        self.update_info = UpdateInformation(file_type='bio',tool_path='UpdateBIOS.sh')

    @patch('fall.firmware_updater.get_factory', side_effect=ValueError('err'))
    def test_raise_invalid_os(self, mock_factory):
        with self.assertRaisesRegex(FallError, 'err'):
            FirmwareUpdater._get_os_factory(OsType.Linux)

    @patch('fall.platform_finder.LinuxPlatformFinder.get')
    def test_successfully_query_all(self, mock_get):
        mock_get.return_value=PlatformInformation(bios_release_date='2022-01-01', bios_vendor='Intel',
                                            bios_version='1.2.3', platform_mfg='Intel', platform_name='kmb-m2')
        expected = Result(200, "SUCCESSFUL QUERY")
        self.assertEqual(self.fw_updater.query('all'), expected)

    @patch('fall.firmware_updater.get_host_os', side_effect=ValueError)
    def test_unsuported_os_query_cmd(self, mock_os):
        self.assertEqual(self.fw_updater.query('all'), UNSUPPORTED_OS_FAILURE)

    @patch('fall.platform_finder.LinuxPlatformFinder.get', side_effect=FallError)
    def test_unable_to_get_platform_info_query(self, mock_platform_finder):
        self.assertEqual(self.fw_updater.query('all'), UNABLE_TO_GET_PLATFORM_INFO_FAILURE)

    @patch('fall.rebooter.LinuxRebooter.reboot')
    @patch('fall.installer.LinuxInstaller.install')
    @patch('fall.configuration_finder.ConfigurationFinder.find_match')
    @patch('fall.configuration_finder.ConfigurationFinder.__init__', return_value=None)
    @patch('fall.firmware_updater.UpgradeChecker.is_upgradable')
    @patch('fall.firmware_updater.is_valid_path')
    def test_successfully_update_firmware_auto_fill_true(self, mock_check_path,
                                                         mock_is_upgradable, mock_match_init,
                                                         mock_match_find, mock_install, mock_run):
        mock_match_find.return_value = self.update_info
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, INSTALL_SUCCESS)

    @patch('fall.rebooter.LinuxRebooter.reboot')
    @patch('fall.installer.LinuxInstaller.install')
    @patch('fall.configuration_finder.ConfigurationFinder.find_match')
    @patch('fall.configuration_finder.ConfigurationFinder.__init__', return_value=None)
    @patch('fall.firmware_updater.UpgradeChecker.is_upgradable')
    @patch(VALID_PATH)
    def test_successfully_update_firmware_auto_fill_false(self, mock_check_path,
                                                          mock_is_upgradable, mock_match_init,
                                                          mock_match_find, mock_install, mock_run):
        mock_match_find.return_value = self.update_info
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        bios_vendor=INTEL, platform_name='kmb-evm', platform_manufacturer=INTEL,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=False)
        self.assertEqual(result, INSTALL_SUCCESS)

    @patch(VALID_PATH)
    def test_validation_fail_missing_input_parameter(self, mock_check_path):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        platform_name='kmb-evm', platform_manufacturer=INTEL,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=False)
        self.assertEqual(result, INPUT_VALIDATION_FAILURE)

    @patch('os.path.isdir', return_value=True)
    def test_validation_fail_invalid_path(self, mock_isdir):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, INPUT_VALIDATION_FAILURE)

    @patch('fall.firmware_updater.get_host_os', side_effect=ValueError)
    @patch(VALID_PATH)
    def test_unsupported_os_install(self, mock_check_path, mock_os):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, UNSUPPORTED_OS_FAILURE)

    @patch('fall.firmware_updater.ConfigurationFinder.find_match', side_effect=FallError)
    @patch('fall.configuration_finder.ConfigurationFinder.find_match', side_effect=FallError)
    @patch('fall.configuration_finder.ConfigurationFinder.__init__', return_value=None)
    @patch('fall.firmware_updater.UpgradeChecker.is_upgradable')
    @patch('fall.firmware_updater.is_valid_path')
    def test_correct_error_no_matching_platform(self, mock_path, mock_is_upgradable, mock_match_init,
                                                          mock_match_find, mock_match):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, UNABLE_FIND_MATCHING_PLATFORM)

    @patch('fall.platform_finder.LinuxPlatformFinder.get', side_effect=FallError)
    @patch(VALID_PATH)
    def test_unable_to_determine_platform_install(self, mock_path, mock_platform_finder):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, UNABLE_TO_GET_PLATFORM_INFO_FAILURE)

    @patch('fall.firmware_updater.UpgradeChecker.is_upgradable', side_effect=FallError)
    @patch(VALID_PATH)
    def test_upgrade_check_fails(self, mock_path, mock_is_upgradable):
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, UPGRADE_CHECK_FAILURE)

    @patch('fall.installer.LinuxInstaller.install', side_effect=FallError)
    @patch('fall.configuration_finder.ConfigurationFinder.find_match')
    @patch('fall.configuration_finder.ConfigurationFinder.__init__', return_value=None)
    @patch('fall.firmware_updater.UpgradeChecker.is_upgradable')
    @patch('fall.firmware_updater.is_valid_path')
    def test_install_fails(self, mock_check_path, mock_is_upgradable, mock_match_init,
                                                          mock_match_find, mock_install):
        mock_match_find.return_value = self.update_info
        result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
                                        capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
        self.assertEqual(result, INSTALL_FAILURE)

    # TODO:  Need to figure out how to get failure reboot case with timer.
    # @patch('fall.rebooter.LinuxRebooter.reboot', side_effect=FallError)
    # @patch('fall.installer.LinuxInstaller.install')
    # @patch('fall.firmware_updater.UpgradeChecker.is_upgradable')
    # @patch('fall.firmware_updater.is_valid_path')
    # def test_reboot_fails(self, mock_check_path, mock_is_upgradable, mock_install, mock_reboot):
    #     result = self.fw_updater.update(path_to_update_package=BIOS_LOCATION,
    #                                     capsule_release_date=RELEASE_DATE, autofill_platform_info=True)
    #     sleep(2)
    #     self.assertEqual(result, REBOOT_FAILURE)

    def test_raise_bios_vendor_is_none(self):
        with self.assertRaisesRegex(ValueError, "BIOS Vendor is required when AutoFill flag is False"):
            self.fw_updater._add_platform_info(None, 'kmb-evm', INTEL)

    def test_raise_platform_name_is_none(self):
        with self.assertRaisesRegex(ValueError, "Platform Name is required when AutoFill flag is False"):
            self.fw_updater._add_platform_info(INTEL, None, INTEL)

    def test_raise_manufacturer_is_none(self):
        with self.assertRaisesRegex(ValueError, "Manufacturer is required when AutoFill flag is False"):
            self.fw_updater._add_platform_info(INTEL, 'kmb-evm', None)

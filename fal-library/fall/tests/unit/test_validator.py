from unittest import TestCase
from mock import patch

from fall.utility.validator import validate_release_date, is_valid_path, validate_guid, \
    validate_user_string_input, clean_input
from fall.platform_info import PlatformInformation
from fall.fall_error import SecurityError
from fall.host_os import OsType


class TestFirmwareUpdater(TestCase):

    def setUp(self):
        self.platform_info = PlatformInformation()

    def test_clean_input(self):
        self.assertEqual(clean_input('\x00Hello<\x00There&You"\x00'), 'Hello&lt;There&amp;You&quot;')

    def test_good_release_date(self):
        self.assertEqual('2022-06-12', validate_release_date('2022-06-12'))

    def test_release_date_error(self):
        with self.assertRaisesRegex(ValueError, "time data '2022-12' does not match format '%Y-%m-%d'"):
            validate_release_date("2022-12")

    def test_not_raise_on_good_input_string(self):
        try:
            validate_user_string_input('Intel_- Corp.', 'BIOS Vendor')
        except Exception as e:
            self.fail(f'Exception raised when not expected: {e}')

    def test_raise_string_too_large(self):
        with self.assertRaisesRegex(ValueError, "BIOS Vendor is too long.  Must be less than 50 characters"):
            validate_user_string_input('TheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedARedCar', 'BIOS Vendor')

    def test_raise_invalid_characters_in_user_string(self):
        with self.assertRaisesRegex(ValueError, "Invalid character in BIOS Vendor"):
            validate_user_string_input('Intel Corp.$', 'BIOS Vendor')

    @patch('fall.utility.validator.os.path.isdir', return_value=False)
    @patch('fall.utility.validator.os.path.islink', return_value=False)
    @patch('fall.utility.validator.os.path.exists', return_value=True)
    def test_valid_path(self, mock_exists, mock_islink, mock_isdir):
        try:
            is_valid_path('/var/cache/manageability/patch.bin', OsType.Linux)
        except Exception as e:
            self.fail(f'Exception raised when not expected: {e}')

    def test_path_invalid_format(self):
        with self.assertRaisesRegex(ValueError, "Invalid Linux path format"):
            is_valid_path('var/cache/manageability/patch.bin', OsType.Linux)

    def test_raise_path_too_large(self):
        with self.assertRaisesRegex(ValueError, "Capsule Path is too long.  Must be less than 500 characters"):
            is_valid_path('TheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedARedCarTheQuickBrownFox'
                          'RanAcrossTheStreetAndNearlyMissedARedCarTheQuickBrownFoxRanAcrossTheStreet'
                          'AndNearlyMissedARedCarTheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedARed'
                          'CarTheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedARedCarTheQuickBrownFox'
                          'RanAcrossTheStreetAndNearlyMissedARedCarTheQuickBrownFoxRanAcrossTheStreet'
                          'AndNearlyMissedARedCarTheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedA'
                          'RedCarTheQuickBrownFoxRanAcrossTheStreetAndNearlyMissedARedCarTheQuickBrown'
                          'FoxRanAcrossTheStreetAndNearlyMissedARedCar', OsType.Linux)

    @patch('fall.utility.validator.os.path.isdir', return_value=False)
    @patch('fall.utility.validator.os.path.exists', return_value=False)
    def test_raise_invalid_path(self, mock_exists, mock_isdir):
        with self.assertRaisesRegex(OSError, "Path to file does not exist: /var/cache/manageability/patch.bin"):
            is_valid_path('/var/cache/manageability/patch.bin', OsType.Linux)

    @patch('fall.utility.validator.os.path.isdir', return_value=False)
    @patch('fall.utility.validator.os.path.islink', return_value=True)
    @patch('fall.utility.validator.os.path.exists', return_value=True)
    def test_raise_is_symlink(self, mock_exists, mock_islink, mock_isdir):
        with self.assertRaisesRegex(SecurityError, "Path is a symbolic link: /var/cache/manageability/patch.bin"):
            is_valid_path('/var/cache/manageability/patch.bin', OsType.Linux)

    @patch('fall.utility.validator.os.path.isdir', return_value=True)
    def test_raise_path_is_not_file(self, mock_isdir):
        with self.assertRaisesRegex(OSError,
                                    "Invalid Path.  Path needs to be a file: /var/cache/manageability/"):
            is_valid_path('/var/cache/manageability/', OsType.Linux)

    def test_check_validate_guid_pass(self):
        try:
            validate_guid('6c8e136f-d3e6-4131-ac32-4687cb4abd27')
        except Exception as e:
            self.fail(f"raised unexpectedly! --> {e}")

    def test_fail_guid_check_with_hex_letter(self):
        with self.assertRaisesRegex(ValueError,
                                    "GUID should be 36 characters displayed in five groups in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed."):
            validate_guid('123e4567-h89b-12d3-a456-9AC7CBDCEE52')

    def test_fail_guid_check_too_few_characters(self):
        with self.assertRaisesRegex(ValueError,
                                    "GUID should be 36 characters displayed in five groups in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed."):
            validate_guid('123e4567-h89b-12d3-a456')

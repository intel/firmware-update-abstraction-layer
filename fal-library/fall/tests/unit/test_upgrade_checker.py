from unittest import TestCase

from fall.upgrade_checker import UpgradeChecker
from fall.fall_error import FallError
from fall.platform_info import PlatformInformation

INTEL = 'Intel'
VERSION = 'VERSION'
KMB_EVM = 'kmb-evm'
DATE_FORMAT = '%m/%d/%Y'
DATE = '2022-01-01'


class TestUpgradeChecker(TestCase):

    def setUp(self):
        self.kmb_platform_info = PlatformInformation(bios_release_date=DATE, bios_vendor=INTEL,
                                                     bios_version=VERSION, platform_mfg=INTEL, platform_name=KMB_EVM)

    def test_not_raise_same_product_and_manufacturer(self):
        self._upgrade_checker = UpgradeChecker(self.kmb_platform_info, self.kmb_platform_info)
        try:
            self._upgrade_checker.compare_platform_and_capsule_information()
        except FallError:
            self.fail('Error raised unexpectedly')

    def test_raise_manufacturer_mismatch(self):
        current_info = PlatformInformation(bios_release_date=DATE, bios_vendor=INTEL,
                                           bios_version=VERSION, platform_mfg='Intel Corp', platform_name=KMB_EVM)
        self._upgrade_checker = UpgradeChecker(current_info, self.kmb_platform_info)
        with self.assertRaisesRegex(FallError,
                                    'BIOS is not upgradable. '
                                    'Reason: Capsule Manufacturer and Platform Manufacturer do not match.'):
            self._upgrade_checker.compare_platform_and_capsule_information()

    def test_raise_product_name_mismatch(self):
        current_info = PlatformInformation(bios_release_date=DATE, bios_vendor=INTEL,
                                           bios_version=VERSION, platform_mfg=INTEL, platform_name='kmb-m2')
        self._upgrade_checker = UpgradeChecker(current_info, self.kmb_platform_info)
        with self.assertRaisesRegex(FallError,
                                    'BIOS is not upgradable. '
                                    'Reason: Capsule Product Name and Platform Product Name do not match.'):
            self._upgrade_checker.compare_platform_and_capsule_information()

    def test_raise_vendor_mismatch(self):
        current_info = PlatformInformation(bios_release_date=DATE, bios_vendor=INTEL,
                                           bios_version=VERSION, platform_mfg=INTEL, platform_name='kmb-m2')
        capsule_info = PlatformInformation(bios_release_date=DATE, bios_vendor='Intel Corp',
                                           bios_version=VERSION, platform_mfg=INTEL, platform_name='kmb-m2')
        self._upgrade_checker = UpgradeChecker(current_info, capsule_info)
        with self.assertRaisesRegex(FallError,
                                    'BIOS is not upgradable.  '
                                    'Reason: Capsule Vendor and Platform Vendor do not match.'):
            self._upgrade_checker.compare_platform_and_capsule_information()

    def test_not_raise_upgrade_allowed(self):
        capsule_info = PlatformInformation(bios_release_date='2022-02-01',
                                           bios_vendor=INTEL, bios_version=VERSION, platform_mfg=INTEL,
                                           platform_name=KMB_EVM)
        self._upgrade_checker = UpgradeChecker(self.kmb_platform_info, capsule_info)
        try:
            self._upgrade_checker.check_upgrade_allowed()
        except FallError:
            self.fail('Error raised unexpectedly')

    def test_raise_same_release_date(self):
        self._upgrade_checker = UpgradeChecker(self.kmb_platform_info, self.kmb_platform_info)
        with self.assertRaisesRegex(FallError,
                                    'Firmware Update Aborted as this package has already been applied.'):
            self._upgrade_checker.check_upgrade_allowed()

    def test_raise_capsule_release_date_prior_platform_date(self):
        capsule_info = PlatformInformation(bios_release_date='2021-12-31',
                                           bios_vendor=INTEL, bios_version=VERSION, platform_mfg=INTEL,
                                           platform_name=KMB_EVM)
        self._upgrade_checker = UpgradeChecker(self.kmb_platform_info, capsule_info)
        with self.assertRaisesRegex(FallError,
                                    'Firmware Update Aborted: Capsule release date is before platform release date'):
            self._upgrade_checker.check_upgrade_allowed()

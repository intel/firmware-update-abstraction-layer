from unittest import TestCase

from fall.query import create_query_response
from fall.platform_info import PlatformInformation

INTEL = 'Intel'
VERSION = 'VERSION'
KMB_EVM = 'kmb-evm'
DATE_FORMAT = '%m/%d/%Y'


class TestQuery(TestCase):

    def test_query_hw(self):
        platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor=INTEL,
                                            bios_version=VERSION, platform_mfg=INTEL, platform_name=KMB_EVM)
        fw = {"bios_release_date": '2022-01-01',
              "bios_vendor": INTEL,
              "bios_version": VERSION
              }
        self.assertEqual(create_query_response('fw', platform_info), str(fw))

    def test_query_fw(self):
        platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor=INTEL,
                                            bios_version=VERSION, platform_mfg=INTEL, platform_name=KMB_EVM)
        hw = {"manufacturer": INTEL,
              "platform_name": KMB_EVM,
              }
        self.assertEqual(create_query_response('hw', platform_info), str(hw))

    def test_query_all(self):
        platform_info = PlatformInformation(bios_release_date='2022-01-01', bios_vendor=INTEL,
                                            bios_version=VERSION, platform_mfg=INTEL, platform_name=KMB_EVM)
        all_param = {"bios_release_date": '2022-01-01',
                     "bios_vendor": INTEL,
                     "bios_version": VERSION,
                     "manufacturer": INTEL,
                     "platform_name": KMB_EVM,
                     }
        self.assertEqual(create_query_response('all', platform_info), str(all_param))

"""
    Checks if Host system is a candidate for the firmware upgrade.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
from datetime import datetime

from .platform_info import PlatformInformation
from .fall_error import FallError

logger = logging.getLogger(__name__)


class UpgradeChecker(object):
    """Base class for performing checks to see if the system is upgradable to the
    new Firmware.

    @param current_info: current platform information
    @param capsule_info: new firmware capsule information
    """

    def __init__(self, current_info: PlatformInformation, capsule_info: PlatformInformation) -> None:
        self._current_info = current_info
        self._capsule_info = capsule_info

    def is_upgradable(self) -> None:
        """Check if system is upgradable to the new Firmware"""
        self.compare_platform_and_capsule_information()
        self.check_upgrade_allowed()

    def compare_platform_and_capsule_information(self) -> None:
        if not self._capsule_info.platform_mfg == self._current_info.platform_mfg:
            logger.debug(f"capsule mfg={self._capsule_info.platform_mfg} "
                         f"platform mfg={self._current_info.platform_mfg}")
            raise FallError(
                'BIOS is not upgradable. Reason: Capsule Manufacturer and Platform Manufacturer do not match.')
        if not self._capsule_info.platform_name == self._current_info.platform_name:
            logger.debug(
                f"capsule platform name={self._capsule_info.platform_name} "
                f"platform name={self._current_info.platform_name}")
            raise FallError(
                'BIOS is not upgradable. Reason: Capsule Product Name and Platform Product Name do not match.')
        if not self._capsule_info.bios_vendor == self._current_info.bios_vendor:
            logger.debug(
                f"capsule vendor={self._capsule_info.bios_vendor} platform vendor={self._current_info.bios_vendor}")
            raise FallError(
                'BIOS is not upgradable.  Reason: Capsule Vendor and Platform Vendor do not match.')
        logger.debug("Manufacturer/Product check passed successfully")

    def check_upgrade_allowed(self) -> None:
        """Check if manifest vendor name matches platform BIOS vendor and
        manifest release date is higher than BIOS release date
        """
        logger.debug(" ")
        try:
            current_release_date = datetime.strptime(
                self._current_info.bios_release_date, '%Y-%m-%d')
            capsule_release_date = datetime.strptime(
                self._capsule_info.bios_release_date, '%Y-%m-%d')
        except ValueError:
            raise FallError('Issue converting date to datetime object')

        if capsule_release_date > current_release_date:
            cf_message = f"""Current info: BIOS Release Date: {self._current_info.bios_release_date},
                                          BIOS Vendor: {self._current_info.bios_vendor},
                                          Platform Manufacturer: {self._current_info.platform_mfg},
                                          Platform Product: {self._current_info.platform_name}"""  # noqa

            nf_message = f"""Capsule info: BIOS Release Date: {self._capsule_info.bios_release_date},
                                          BIOS Vendor: {self._capsule_info.bios_vendor},
                                          Platform Manufacturer: {self._capsule_info.platform_mfg},
                                          Platform Product: {self._capsule_info.platform_name}"""  # noqa
            logger.info(cf_message)
            logger.info(nf_message)
        elif self._capsule_info.bios_release_date == self._current_info.bios_release_date:
            logger.debug(f"Firmware already applied: date:{self._current_info.bios_release_date}")
            raise FallError('Firmware Update Aborted as this package has already been applied.')
        else:
            logger.info(f'Current Info: BIOS Release Date: {self._current_info.bios_release_date}')  # noqa
            logger.info(f'Capsule Info: BIOS Release Date: {self._capsule_info.bios_release_date}')
            raise FallError(
                'Firmware Update Aborted: Capsule release date is before platform release date')

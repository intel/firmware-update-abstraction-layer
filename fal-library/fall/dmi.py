"""
    Use Linux dmi path to gather system information.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import os
import logging

from datetime import datetime

from .utility.file_handler import read_file
from .constants import UNKNOWN
from .platform_info import PlatformInformation


logger = logging.getLogger(__name__)


FW_DMI_PATH = '/sys/devices/virtual/dmi/id/'
DMI_BIOS_RELEASE_DATE = 'bios_date'
DMI_BIOS_VENDOR = 'bios_vendor'
DMI_BIOS_VERSION = 'bios_version'
DMI_SYSTEM_MANUFACTURER = 'sys_vendor'
DMI_SYSTEM_PRODUCT_NAME = 'product_name'
FW_DMI_IT_PATH = '/scripts/dmi_id_bios_info/'


def get_dmi_system_info() -> PlatformInformation:
    """Reads the system information from Linux Dmi path

    @return: BIOS release date, BIOS vendor, BIOS version, Manufacturer, Product
    of the platform
    """
    path = FW_DMI_IT_PATH if os.path.isdir(FW_DMI_IT_PATH) else FW_DMI_PATH

    bios_release_date = _parse_release_date(
        read_file(path + DMI_BIOS_RELEASE_DATE, UNKNOWN))
    bios_vendor = read_file(
        path + DMI_BIOS_VENDOR, UNKNOWN)
    bios_version = read_file(
        path + DMI_BIOS_VERSION, UNKNOWN)
    platform_mfg = read_file(
        path + DMI_SYSTEM_MANUFACTURER, "")
    platform_product = read_file(
        path + DMI_SYSTEM_PRODUCT_NAME, "")

    if UNKNOWN in [bios_vendor, bios_version]:
        logger.debug(
            "return_value: bios_vendor:{}, bios_version:{},"
            " bios_release_date:{}, platform_mfg: {}, platform_product:{}". format(
                bios_vendor,
                bios_version,
                bios_release_date,
                platform_mfg,
                platform_product))
        return PlatformInformation()
    return PlatformInformation(bios_release_date, bios_vendor,
                               bios_version, platform_mfg, platform_product)


def _parse_release_date(date_to_format: str) -> str:
    """Method to parse the string to retrieve the date.  Converts the DMI
    string format into the preferred format.

    @param date_to_format: date that needs to be formatted
    @return: Formatted date
    @raises: ValueError when format is not matched to the ones specified
    """
    for fmt in ("%m/%d/%Y", "%b %d %Y"):
        try:
            datetime_format = datetime.strptime(date_to_format, fmt)
            return datetime_format.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError('Time date does not match anything')

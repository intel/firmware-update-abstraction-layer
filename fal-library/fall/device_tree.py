"""
    Use Linux device-tree path to gather system information.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging

from datetime import datetime

from .constants import UNKNOWN
from .utility.file_handler import read_file
from .platform_info import PlatformInformation


logger = logging.getLogger(__name__)

BIOS_RELEASE_DATE = 'bios-release-date'
BIOS_VENDOR = 'bios-vendor'
BIOS_VERSION = 'bios-version'
SYSTEM_MANUFACTURER = 'system-manufacturer'
SYSTEM_PRODUCT_NAME = 'system-product-name'
FW_DEVICE_TREE_PATH = '/proc/device-tree/firmware/bios/'


def get_device_tree_system_info() -> PlatformInformation:
    """Reads the system information using Linux Device Tree

    @return: Platform Information
    """
    bios_release_date = _parse_bios_date(
        read_file(FW_DEVICE_TREE_PATH + BIOS_RELEASE_DATE, UNKNOWN))
    bios_vendor = read_file(
        FW_DEVICE_TREE_PATH + BIOS_VENDOR, UNKNOWN)
    bios_version = read_file(
        FW_DEVICE_TREE_PATH + BIOS_VERSION, UNKNOWN)
    platform_mfg = read_file(
        FW_DEVICE_TREE_PATH + SYSTEM_MANUFACTURER, "")
    platform_product = read_file(
        FW_DEVICE_TREE_PATH + SYSTEM_PRODUCT_NAME, "")
    return PlatformInformation(bios_release_date, bios_vendor,
                               bios_version, platform_mfg, platform_product)


def _parse_bios_date(date_to_format: str) -> str:
    """Method to parse the string to retrieve date

    @param date_to_format:: date to be parsed
    @return: Formatted date
    @raises: ValueError when format is not matched to the one specified
    """
    for fmt in ["%b %d %Y %H:%M:%S"]:
        try:
            datetime_format = datetime.strptime(date_to_format, fmt)
            return datetime_format.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f'Time date \'{date_to_format}\' does not match expected format')

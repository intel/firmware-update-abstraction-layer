"""
    Finds the matching platform information

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging

from typing import Dict

from .platform_info import PlatformInformation
from .update_info import UpdateInformation
from .xml_handler import XmlHandler
from .fall_error import FallError
from .utility.validator import clean_input

logger = logging.getLogger(__name__)

PLATFORM_INFO_XML_FILE = '/usr/share/fall/firmware_info.db'
PLATFORM_INFO_SCHEMA_FILE = '/usr/share/fall/firmware_schema.xsd'


class ConfigurationFinder(object):
    """Finds the matching platform configuration in the XML database file"""

    def __init__(self, platform_information: PlatformInformation,
                 xml: str = PLATFORM_INFO_XML_FILE, schema: str = PLATFORM_INFO_SCHEMA_FILE) -> None:
        self._platform_info = platform_information
        self._platform_name = platform_information.platform_name
        self._xml_file = XmlHandler(xml=xml, is_file=True, schema_location=schema)

    def find_match(self) -> UpdateInformation:
        update_info = UpdateInformation()
        platform_info = self._get_platform_elements()
        update_info.tool_args = clean_input(platform_info.get('firmware_tool_args', ''))
        update_info.file_type = clean_input(platform_info.get('firmware_file_type', ''))
        update_info.tool_path = clean_input(platform_info.get('firmware_tool', ''))
        update_info.firmware_destination = clean_input(platform_info.get('firmware_dest_path', ''))
        update_info.firmware_tool_check_args = clean_input(platform_info.get('firmware_tool_check_args', ''))

        update_info.platform_info = self._platform_info
        update_info.tool_options = clean_input(platform_info.get('tool_options', ''))
        update_info.is_guid_required = self._is_guid_required()
        return update_info

    def _get_platform_elements(self) -> Dict:
        platforms = self._xml_file.get_root_elements('firmware_product', 'name')
        logger.debug(f"Available Platforms: {platforms}")
        if self._platform_info.platform_name not in platforms:
            raise FallError(
                f"The platform is unsupported - {self._platform_name}")

        logger.debug(f"Platform information available: {self._platform_name}")

        return self._xml_file.get_children(
            f"firmware_product[@name='{self._platform_name}']")

    def _is_guid_required(self) -> bool:
        try:
            is_guid_required = self._xml_file.get_attribute(
                f"firmware_product[@name='{self._platform_name}']", 'guid')
            return bool(is_guid_required)
        except KeyError:
            return False

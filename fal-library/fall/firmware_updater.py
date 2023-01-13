"""
    Platform Firmware Update Tool

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging

from .result_constants import Result, UNSUPPORTED_OS_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE, \
    UNABLE_FIND_MATCHING_PLATFORM, INPUT_VALIDATION_FAILURE, UPGRADE_CHECK_FAILURE, INSTALL_FAILURE, \
    REBOOT_FAILURE, INSTALL_SUCCESS, QUERY_SUCCESS

from typing import Any, Optional
from datetime import date

from .platform_info import PlatformInformation
from .upgrade_checker import UpgradeChecker
from .os_factory import OsFactory, get_factory
from .utility.validator import validate_release_date, is_valid_path, validate_user_string_input, validate_guid
from .query import create_query_response
from .configuration_finder import ConfigurationFinder

from .host_os import get_host_os, OsType
from .fall_error import SecurityError, FallError
from .utility.file_handler import log_error
from .xml_handler import XmlException
from threading import Timer
logger = logging.getLogger(__name__)


class FirmwareUpdater:
    """API for Platform Firmware Update tool"""

    def __init__(self) -> None:
        logger.info('This library uses the following:')
        logger.info('     defusedxml - PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2 '
                    '- Copyright (c) 2013-2017 by Christian Heimes <christian@python.org>\n\n')
        self._capsule_info = PlatformInformation()
        self._platform_info = PlatformInformation()

    @staticmethod
    def _get_os_factory(host_os: OsType) -> OsFactory:
        try:
            return get_factory(host_os)
        except ValueError as e:
            log_error(e)
            raise FallError(e)

    @staticmethod
    def _get_platform_info(os_type: OsFactory) -> PlatformInformation:
        platform_finder = os_type.create_platform_finder()
        try:
            return platform_finder.get()
        except (ValueError, FallError) as e:
            log_error(e)
            raise FallError(e)

    def query(self, option_type: str = 'all') -> Result:
        """Queries the platform info and returns the result

        @param option_type: type of information to return.  FW, HW, ALL
        @return: Result and on success the result of the query
        """

        try:
            host_os = get_host_os()
            os_factory = FirmwareUpdater._get_os_factory(host_os)
        except(FallError, ValueError):
            return UNSUPPORTED_OS_FAILURE

        try:
            self._platform_info = FirmwareUpdater._get_platform_info(os_factory)
        except FallError:
            return UNABLE_TO_GET_PLATFORM_INFO_FAILURE

        query_response = str(create_query_response(option_type, self._platform_info))
        logger.info(f'Query response: {query_response}')

        return QUERY_SUCCESS

    def update(self, path_to_update_package: str, capsule_release_date: Optional[str] = None,   # noqa
               bios_vendor: Optional[str] = None, platform_name: Optional[str] = None,
               platform_manufacturer: Optional[Any] = None, hash_algorithm: Optional[int] = None,
               guid: Optional[str] = None, autofill_platform_info: bool = False) -> Result:
        """Checks if the platform info needs to be automatically filled or not.
        raise error and return for invalid user inputs.

        @param path_to_update_package: path to package
        @param capsule_release_date: release date from user of update capsule
        @param bios_vendor: BIOS vendor name
        @param platform_name: platform name
        @param platform_manufacturer:platform manufacturer
        @param hash_algorithm: 384 or 512 or None (if not used)
        @param autofill_platform_info: True if platform information needs
        @param guid: GUID when required by platform.
        to be automatically filled using information from the system
        @return Result code and message
        """
        # Input Validation Check
        try:
            host_os = get_host_os()
        except ValueError as e:
            log_error(e)
            return UNSUPPORTED_OS_FAILURE

        try:
            validate_user_string_input(bios_vendor, 'BIOS Vendor')
            validate_user_string_input(platform_name, 'Platform Name')
            validate_user_string_input(platform_manufacturer, 'Manufacturer')
            validate_guid(guid)
            is_valid_path(path_to_update_package, host_os)
            release_date = validate_release_date(date.today().strftime("%Y-%m-%d"))
            if capsule_release_date:
                release_date = validate_release_date(capsule_release_date)

            if not autofill_platform_info:
                self._add_platform_info(bios_vendor, platform_name, platform_manufacturer)
                self._capsule_info.bios_release_date = release_date

        except (ValueError, OSError, SecurityError) as e:
            log_error(e)
            return INPUT_VALIDATION_FAILURE

        # OS Check
        try:
            os_factory = FirmwareUpdater._get_os_factory(host_os)
        except FallError:
            return UNSUPPORTED_OS_FAILURE

        try:
            self._platform_info = FirmwareUpdater._get_platform_info(os_factory)
        except FallError:
            return UNABLE_TO_GET_PLATFORM_INFO_FAILURE

        if autofill_platform_info:
            self._capsule_info.bios_vendor = self._platform_info.bios_vendor
            self._capsule_info.platform_mfg = self._platform_info.platform_mfg
            self._capsule_info.platform_name = self._platform_info.platform_name
            self._capsule_info.bios_release_date = release_date

        # Upgrade Checker
        try:
            UpgradeChecker(self._platform_info, self._capsule_info).is_upgradable()
        except FallError as e:
            log_error(e)
            return UPGRADE_CHECK_FAILURE

        # Find the matching platform in the configuration file
        try:
            update_info = ConfigurationFinder(self._platform_info).find_match()
            update_info.guid = guid
        except (FallError, XmlException) as e:
            log_error(e)
            return UNABLE_FIND_MATCHING_PLATFORM

        # Install
        installer = os_factory.create_installer()
        # TODO: Check hash algorithm matches supported values 384 and 512
        try:
            installer.install(path_to_update_package, update_info, hash_algorithm)
        except FallError as e:
            log_error(e)
            return INSTALL_FAILURE

        # Reboot
        def trigger_reboot() -> None:
            """This method triggers a reboot."""
            logger.info("reboot")
            os_factory.create_rebooter().reboot()
        try:
            time_to_trigger_reboot = Timer(0.1, trigger_reboot)
            time_to_trigger_reboot.start()
        except FallError as e:
            log_error(e)
            return REBOOT_FAILURE

        return INSTALL_SUCCESS

    def _add_platform_info(self, bios_vendor: Optional[str], platform_name: Optional[str],
                           platform_mfg: Optional[str]):
        if bios_vendor is None:
            raise ValueError("BIOS Vendor is required when AutoFill flag is False")
        if platform_name is None:
            raise ValueError("Platform Name is required when AutoFill flag is False")
        if platform_mfg is None or not isinstance(platform_mfg, str):
            raise ValueError("Manufacturer is required when AutoFill flag is False")

        self._capsule_info.bios_vendor = bios_vendor
        self._capsule_info.platform_name = platform_name
        self._capsule_info.platform_mfg = platform_mfg

"""
    Command classes to represent command entered by user.

    # Copyright (C) 2022-2023 Intel Corporation
    # SPDX-License-Identifier: Apache-2.0
"""
import argparse
import logging

from abc import ABC, abstractmethod
from fall.firmware_updater import FirmwareUpdater
from fall.result_constants import INSTALL_SUCCESS, INPUT_VALIDATION_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE, \
    UPGRADE_CHECK_FAILURE, INSTALL_FAILURE, REBOOT_FAILURE, UNSUPPORTED_OS_FAILURE, QUERY_SUCCESS, Result

from falc.falc_exception import FalcException
from falc.utility import search_keyword, get_canonical_representation_of_path
from falc.constant import QUERY, FW

COMMAND_FAIL = "FAIL"
COMMAND_SUCCESS = "SUCCESS"
CACHE = '/var/cache/manageability/repository-tool/'
FW_SUCCESS_MESSAGE_LIST = [INSTALL_SUCCESS]
FW_FAILURE_MESSAGE_LIST = [INPUT_VALIDATION_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE,
                           UPGRADE_CHECK_FAILURE, INSTALL_FAILURE, REBOOT_FAILURE, UNSUPPORTED_OS_FAILURE]
QUERY_SUCCESS_MESSAGE_LIST = [QUERY_SUCCESS]
QUERY_FAILURE_MESSAGE_LIST = [UNSUPPORTED_OS_FAILURE, UNABLE_TO_GET_PLATFORM_INFO_FAILURE]

logger = logging.getLogger(__name__)


class Command(ABC):  # pragma: no cover
    """Base class for command objects

    @param cmd_type: name of command to execute
    """

    def __init__(self, cmd_type: str) -> None:
        self._cmd_type = cmd_type

    @abstractmethod
    def trigger_command(self, args: argparse.Namespace) -> int:
        """Trigger the command-line utility tool to invoke update.
        @return: process return code"""
        pass


class FwCommand(Command):
    def __init__(self) -> None:
        """FW command"""
        super().__init__(FW)

    def trigger_command(self, user_input: argparse.Namespace) -> int:  # no pragma cover
        """Trigger the command-line utility tool to invoke update.

        @param user_input: arguments passed to command-line tool.
        @return: exit code for command (0 success, 1 fail)
        """
        payload = FirmwareUpdater().update(path_to_update_package=get_canonical_representation_of_path(user_input.path),
                                           capsule_release_date=user_input.releasedate, bios_vendor=user_input.vendor,
                                           platform_name=user_input.product,
                                           platform_manufacturer=user_input.manufacturer, guid=user_input.guid,
                                           autofill_platform_info=user_input.autofill)
        return self.search_response(payload)

    def search_response(self, payload: Result) -> int:
        """Search for keywords in response message

        @param payload: payload received in which to search
        @return: exit code for command (0 success, 1 fail)
        """
        if search_keyword(payload, FW_SUCCESS_MESSAGE_LIST):
            logger.info(f"\n {self._cmd_type.upper()} Command Execution is Completed")
            return 0
        elif search_keyword(payload, FW_FAILURE_MESSAGE_LIST):
            logger.error(f"\n {self._cmd_type.upper()} Command Execution FAILED")
            return 1
        else:
            raise FalcException('Unable to determine if FW operation is success or failure')


class QueryCommand(Command):
    def __init__(self) -> None:
        """Query command"""
        super().__init__(QUERY)

    def trigger_command(self, user_option: argparse.Namespace) -> int:   # no pragma cover
        """Trigger the command-line utility tool to invoke query request.
        @param user_option:query type to return
        @return: exit code for command (0 success, 1 fail)
        """
        logger.debug(f"command={user_option}")

        payload = FirmwareUpdater().query(user_option.option)
        return self.search_response(payload)

    def search_response(self, payload: Result) -> int:
        """Search for keywords in response message

        @param payload: payload received in which to search
        @return: exit code for command (0 success, 1 fail)
        """
        logger.debug("query search response")
        if search_keyword(payload, QUERY_SUCCESS_MESSAGE_LIST):
            logger.info(f"\n {self._cmd_type.upper()} Command Execution is Completed")
            return 0
        elif search_keyword(payload, QUERY_FAILURE_MESSAGE_LIST):
            logger.error(f"\n {self._cmd_type.upper()} Command Execution FAILED")
            return 1
        else:
            raise FalcException(f'Unable to determine if query operation is success or failure')

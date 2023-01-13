"""
    Firmware Update based on BIOS install type

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
import os

from abc import ABC
from typing import Optional
from pathlib import Path

from .utility.shell_runner import PseudoShellRunner
from .utility.file_handler import move_file
from .update_info import UpdateInformation
from .packagemanager.irepo import IRepo
from .constants import AFULNX_64, DOCKER_CHROOT_PREFIX
from .fall_error import FallError

logger = logging.getLogger(__name__)


class BiosFactory(ABC):
    """Abstract Factory for creating the concrete classes based on the BIOS
    on the platform.

    @param update_info: platform update information
    """

    def __init__(self, repo: IRepo, update_info: UpdateInformation) -> None:
        self._repo: IRepo = repo
        self._update_info = update_info
        self._runner = PseudoShellRunner()

    def install(self, package_name: str, hash_algorithm: Optional[int] = None) -> None: # pragma: no cover
        """Extracts files from the downloaded package and delete the files after the update

        @param package_name: name of package to install
        @param hash_algorithm: hash algorithm used -> 384 or 512
        """
        pass

    @staticmethod
    def get_factory(repo: IRepo, update_info: UpdateInformation) -> "BiosFactory":
        """Checks if the current platform is supported or not

        @param repo: representation of repository path
        @param update_info: information required to perform the update
        """
        return LinuxFileFirmware(repo, update_info) if update_info.firmware_destination \
            else LinuxToolFirmware(repo, update_info)


class LinuxToolFirmware(BiosFactory):
    """Derived class constructor invoking base class constructor for
    Linux devices that use Firmware tool to perform the update.

    @param repo: string representation of repository path
    @param update_info: platform update information
    """

    def __init__(self, repo: IRepo, update_info: UpdateInformation) -> None:
        super().__init__(repo, update_info)

    def _parse_guid(self, output: str) -> Optional[str]:
        """Parses the shell command output to retrieve the value of system firmware type

        @param output: shell command output of firmware tool
        @return: system firmware type is present if not return None
        """
        for line in output.splitlines():
            if "System Firmware type" in line or "system-firmware type" in line:
                return line.split(',')[1].split()[0].strip('{').strip('}')
        return None

    def _extract_guid(self) -> str:
        """Method to get system firmware type

        @return: None or GUID
        """
        (out, err, code) = PseudoShellRunner.run(f'{self._update_info.tool_path} -l')
        if code != 0:
            raise FallError(f"Firmware Update Aborted: failed to list GUIDs: {err}")
        guid = self._parse_guid(out)
        logger.debug("GUID : " + str(guid))
        if not guid:
            raise FallError("Firmware Update Aborted: No System Firmware type GUID found")
        return guid

    def _apply_firmware(self, fw_file: str) -> None:
        """Updates firmware on the platform by calling the firmware update tool

        @param fw_file: firmware file name
        @raises FallError: on failed firmware attempt
        """
        guid = ""
        if self._update_info.is_guid_required:
            guid = self._update_info.guid if self._update_info.guid else self._extract_guid()
        tool_args = self._update_info.tool_args if self._update_info.tool_args else ''
        tool_options = self._update_info.tool_options if self._update_info.tool_options else ''
        logger.debug(f"GUID={guid}, Tool Args={tool_args}, Tool options={tool_options}")

        cmd = self._update_info.tool_path + " " + tool_args + " " + str(guid) + " " \
              + str(Path(self._repo.name()) / fw_file) + " " + tool_options
        logger.info(f"firmware command: {cmd}")

        logger.debug(f"Applying Firmware: Using FW tool: {self._update_info.tool_path}")
        if self._update_info.tool_path == AFULNX_64:
            logger.info("Device will reboot upon successful firmware install.")
        is_docker_app = os.environ.get("container", False)
        if is_docker_app:
            logger.debug(f"APP ENV : {is_docker_app}")
            (out, err, code) = PseudoShellRunner.run(DOCKER_CHROOT_PREFIX + cmd)
        else:
            (out, err, code) = PseudoShellRunner.run(cmd)
        if code == 0:
            logger.info("Apply firmware command successful.")
        else:
            logger.debug(out)
            logger.debug(err)
            if err == '':
                err = "Firmware command failed"
            raise FallError(str(err))

    def install(self, package_name: str, hash_algorithm: Optional[int] = None) -> None:
        """Extracts files from the downloaded package and delete the files after the update

        @param package_name: name of package to install
        @param hash_algorithm: hash algorithm used -> 384 or 512
        """
        if '/' in self._update_info.tool_path:
            if not os.path.isfile(self._update_info.tool_path):
                raise FallError(
                    f"Firmware Update Aborted:  Firmware tool does not exist at {self._update_info.tool_path}")

        if self._update_info.firmware_tool_check_args:
            runner = PseudoShellRunner()
            cmd = self._update_info.tool_path + " " + self._update_info.firmware_tool_check_args
            (out, err, code) = runner.run(cmd)
            if code != 0:
                raise FallError(f"Firmware Update Aborted: Firmware tool: {err}")

        try:
            self._apply_firmware(package_name)
        except (ValueError, TypeError) as e:
            raise FallError(str(e))


class LinuxFileFirmware(BiosFactory):
    """Derived class constructor invoking base class constructor for
    Linux devices that use Firmware file to update firmware.

    @param update_info: platform update information
    """

    def __init__(self, repo: IRepo, update_info: UpdateInformation) -> None:
        super().__init__(repo, update_info)

    def install(self, pkg_filename: str, hash_algorithm: Optional[int] = None) -> None:
        """Extracts files from the downloaded package and applies firmware update and deletes the
        files after the update

        @param pkg_filename: downloaded package filename
        @param hash_algorithm: hash algorithm used -> 384 or 512
        @raises FallError:  failed firmware attempt
        """

        logger.debug(f"pkg_filename={pkg_filename}")
        try:
            source_path = str(Path(self._repo.name()) / pkg_filename[:-3]) + 'fv'
            if not self._update_info.firmware_destination:
                raise FallError("Firmware destination is required.")
            move_file(source_path, self._update_info.firmware_destination)
        except (OSError, IOError) as e:
            logger.debug(str(e))
            raise FallError(f"Firmware Update Aborted: File copy to path failed: {e}")

        logger.debug("Firmware Update: File successfully moved, new path: {}".format(
            self._update_info.firmware_destination))

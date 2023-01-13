"""
    Installs new Firmware on the Host system

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
import os

from abc import ABC, abstractmethod
from typing import Optional

from .packagemanager.local_repo import DirectoryRepo
from .fall_error import FallError
from .update_info import UpdateInformation
from .bios_factory import BiosFactory

logger = logging.getLogger(__name__)


class Installer(ABC):
    """Base class for installing the new Firmware."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def install(self, path_to_package: str, update_info: UpdateInformation,
                hash_algorithm: Optional[int] = None) -> None:
        """Performs a Firmware update.

        @param path_to_package: Path to install package
        @param update_info: Update Information of matching platform in firmware_info.db file
        @param hash_algorithm: hash algorithm used -> 384 or 512
        """
        pass


class LinuxInstaller(Installer):
    """Derived class. Installs new Firmware on a Linux OS."""

    def __init__(self) -> None:
        super().__init__()

    def install(self, path_to_package: str, update_info: UpdateInformation,
                hash_algorithm: Optional[int] = None) -> None:
        """Performs a Linux Firmware update.

        @param path_to_package: Path to install package
        @param update_info: Update Information of matching platform in firmware_info.db file
        @param hash_algorithm: hash algorithm used -> 384 or 512
        """
        if update_info.platform_info is None:
            raise FallError("Platform Information unspecified")

        if update_info.platform_info.platform_name == "":
            raise FallError("Platform product unspecified.")
        repo = DirectoryRepo(os.path.dirname(path_to_package))
        pkg_file_name = os.path.basename(path_to_package)
        factory = BiosFactory.get_factory(repo, update_info)
        factory.install(pkg_file_name, hash_algorithm)

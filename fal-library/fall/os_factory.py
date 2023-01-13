"""
    Creates concrete classes based on OS Type of the Host system.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging
from abc import ABC, abstractmethod

from .host_os import OsType
from .platform_finder import PlatformFinder, LinuxPlatformFinder
from .installer import Installer, LinuxInstaller
from .rebooter import Rebooter, LinuxRebooter

logger = logging.getLogger(__name__)


class OsFactory(ABC):
    """Abstract Factory for creating the concrete classes based on the OS
    on the platform.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_platform_finder(self) -> PlatformFinder:
        """Creates and returns an OS specific platform finder to
        automatically get the required system information

        @return OS specific PlatformFinder
        """
        pass

    @abstractmethod
    def create_installer(self) -> Installer:
        """Creates and returns an OS specific installer for firmware update

        @return OS specific Installer
        """
        pass

    @abstractmethod
    def create_rebooter(self) -> Rebooter:
        """Creates and returns an OS specific rebooter for after the firmware update

        @return OS specific Rebooter
        """
        pass


def get_factory(os_type: OsType) -> OsFactory:
    """Gets the correct abstract factory based on the OS detected on the host system

    @param os_type: OS type detected
    @return: Abstract Factory of detected OS
    """
    if os_type == OsType.Linux:
        return LinuxFactory()
    raise ValueError(f'Unsupported OS type: {os_type}.')


class LinuxFactory(OsFactory):
    """Abstract Factory for creating the concrete classes based on the OS
    on the platform.  This instance is for Linux.
    """

    def __init__(self) -> None:
        super().__init__()

    def create_platform_finder(self) -> PlatformFinder:
        """Creates and returns a Linux based platform finder to automatically
         get the required system information

        @return Linux specific PlatformFinder
        """
        return LinuxPlatformFinder()

    def create_installer(self) -> Installer:
        """Creates and returns a Linux based installer for firmware update

        @return Linux specific Installer
        """
        return LinuxInstaller()

    def create_rebooter(self) -> Rebooter:
        """Creates and returns a Linux based rebooter for after the firmware update

        @return Linux specific Rebooter
        """
        return LinuxRebooter()

"""
    Finds the platform information in the event the user sets autofill_platform_info=True.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging
from abc import ABC, abstractmethod
from .platform_info import PlatformInformation
from .dmi import get_dmi_system_info
from .device_tree import get_device_tree_system_info
from .utility.file_handler import is_path_exist

logger = logging.getLogger(__name__)

DMI_PATH = '/sys/devices/virtual/dmi/'


class PlatformFinder(ABC):
    """Base class for finding platform information.

    @capsule_release_date: release date from user of update capsule
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self) -> PlatformInformation:
        pass


class LinuxPlatformFinder(PlatformFinder):
    """Derived class. Finds the platform information"""

    def __init__(self) -> None:
        super().__init__()

    def get(self) -> PlatformInformation:
        # Check if DMI path exists
        if is_path_exist(DMI_PATH):
            return get_dmi_system_info()
        return get_device_tree_system_info()

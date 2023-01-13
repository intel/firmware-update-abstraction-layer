"""
    Detect the host Operating system.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
import platform
import os

from enum import Enum, unique


logger = logging.getLogger(__name__)


@unique
class OsType(Enum):
    """Supported Operating Systems."""
    Linux = 0
    # Windows = 1 # Not currently supported


def get_host_os() -> OsType:
    """Detects the operating system type running on the host system
    Will detect host OS if in container only for Linux distributions that have
    lsb_release working; otherwise falls back to method that cannot see outside
    the container.

    @return: OS type
    """

    if _is_running_container():
        # TODO:  Support running in a container
        return OsType.Linux

    host_os = platform.system()
    if hasattr(OsType, host_os):
        if host_os == OsType.Linux.name:
            return OsType.Linux

    raise ValueError('Unsupported OS Type')


def _is_running_container() -> bool:
    """Detects if the application is running inside container.
    @return: True if the environment is inside container; otherwise, False.
    """
    if os.environ.get("container", False):
        logger.debug("Running inside container.")
        return True
    return False

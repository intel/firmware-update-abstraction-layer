"""
    Reboots the host system after a firmware update

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import os
import logging

from abc import ABC, abstractmethod
from .fall_error import FallError
from .utility.shell_runner import PseudoShellRunner
from .constants import DOCKER_CHROOT_PREFIX

logger = logging.getLogger(__name__)


class Rebooter(ABC):  # pragma: no cover
    """Base class for rebooting the system."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def reboot(self) -> None:
        pass


class LinuxRebooter(Rebooter):
    """Derived class. Reboots the host system on a Linux OS"""

    def __init__(self) -> None:
        pass

    def reboot(self) -> None:
        is_docker_app = os.environ.get("container", False)
        cmd = "/sbin/reboot -f"
        if is_docker_app:
            logger.debug("APP ENV : {}".format(is_docker_app))
            (output, err, code) = PseudoShellRunner.run(DOCKER_CHROOT_PREFIX + cmd)
        else:
            (output, err, code) = PseudoShellRunner.run(cmd)
        if code and code < 0:
            raise FallError(f'Firmware Update Aborted: Reboot Failed: {err}')

"""
    Data structure for Platform Information

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

from dataclasses import dataclass, field
from typing import Optional
from .constants import UNKNOWN


@dataclass(init=True)
class PlatformInformation:
    bios_release_date: str = field(default=UNKNOWN)
    bios_vendor: str = field(default=UNKNOWN)
    bios_version: str = field(default=UNKNOWN)
    platform_mfg: str = field(default="")
    platform_name: str = field(default="")

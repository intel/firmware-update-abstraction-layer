"""
    Data structure for Update Information

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
from dataclasses import dataclass
from typing import Optional
from .platform_info import PlatformInformation


@dataclass(init=True)
class UpdateInformation:
    file_type: str = ""
    platform_info: Optional[PlatformInformation] = None
    firmware_destination: Optional[str] = None
    tool_args: Optional[str] = None
    tool_path: str = ""
    firmware_tool_check_args: Optional[str] = None
    tool_options: Optional[str] = None
    is_guid_required: bool = False
    guid: Optional[str] = None

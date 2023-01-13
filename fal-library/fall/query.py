"""
    Handle Query request
    @copyright: Copyright 2022-2023 Intel Corporation All Rights Reserved.
    @license: Intel, see licenses/LICENSE for more details.
"""
import logging

from .platform_info import PlatformInformation
from enum import Enum, unique, auto

logger = logging.getLogger(__name__)


@unique
class QueryType(Enum):
    """Supported Query Types"""
    FW = auto()
    HW = auto()
    ALL = auto()


def create_query_response(query_type: str, platform_info: PlatformInformation) -> str:
    upper_query_type = query_type.upper()

    if upper_query_type == QueryType.FW.name:
        msg = {"bios_release_date": platform_info.bios_release_date,
               "bios_vendor": platform_info.bios_vendor,
               "bios_version": platform_info.bios_version
               }
        return str(msg)

    if upper_query_type == QueryType.HW.name:
        msg = {"manufacturer": platform_info.platform_mfg,
               "platform_name": platform_info.platform_name,
               }
        return str(msg)

    msg = {"bios_release_date": platform_info.bios_release_date,
           "bios_vendor": platform_info.bios_vendor,
           "bios_version": platform_info.bios_version,
           "manufacturer": platform_info.platform_mfg,
           "platform_name": platform_info.platform_name,
           }
    return str(msg)

"""
    Validates user input

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
import os
import re
import html

from typing import Optional
from datetime import datetime

from fall.fall_error import SecurityError
from fall.host_os import OsType

logger = logging.getLogger(__name__)

MAX_STRING_CHARS = 50
MAX_PATH_CHARS = 500


def validate_release_date(release_date: str) -> str:
    """validates the release date format from user.

    @param release_date: release date from user of update capsule
    """
    datetime_format = datetime.strptime(release_date, "%Y-%m-%d")
    return datetime_format.strftime("%Y-%m-%d")


def validate_user_string_input(user_input: Optional[str], param_name: str) -> None:
    if user_input:
        if len(user_input) >= MAX_STRING_CHARS:
            raise ValueError(f"{param_name} is too long.  Must be less than {MAX_STRING_CHARS} characters")

        if not bool(re.match("[a-zA-Z0-9.()+, _-]+$", user_input)):
            raise ValueError(f"Invalid character in {param_name}")
        logger.debug(f"User input string passed checks for {param_name}")


def is_valid_path(package_path: str, host_os: OsType) -> None:
    """checks if the current path is valid.
    @param package_path: path to install capsule
    @param host_os: OS Type

    @raise ValueError - Regex validation failure
    @raise OSError - Invalid path
    @raise SecurityError - Path is a symbolic link
    """
    if len(package_path) > MAX_PATH_CHARS:
        raise ValueError(f"Capsule Path is too long.  Must be less than {MAX_PATH_CHARS} characters")

    if host_os == OsType.Linux:
        if not bool(re.match("^/|(/[a-zA-Z0-9_-]+)+$", package_path)):
            raise ValueError("Invalid Linux path format")

    if os.path.isdir(package_path):
        raise OSError(f'Invalid Path.  Path needs to be a file: {package_path}')
    if not os.path.exists(package_path):
        raise OSError(f'Path to file does not exist: {package_path}')
    if os.path.islink(package_path):
        raise SecurityError(f'Path is a symbolic link: {package_path}')


def validate_guid(value: Optional[str]) -> None:
    """Validates that the user inputted string follows the GUID string standard
        @param value: user entered GUID
        @return: entered string if it passes regex check
        @raise argparse.ArgumentTypeError: Invalid guid format
        """
    if value:
        if not bool(re.match("^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$", str(value))):
            raise ValueError(
                f"GUID should be 36 characters displayed in five groups in the format "
                f"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed.")


def clean_input(val: str) -> str:
    """Clean input by escaping special characters and removing null characters

    @param val: input to sanitize
    @return: sanitized value
    """
    val = html.escape(val)
    return str.replace(val, "\x00", "", -1)

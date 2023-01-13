""" User import validation

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import datetime
import argparse
import re


def validate_string_less_than_n_characters(value: str, param_type: str, max_size: int) -> str:
    """Validates that the user inputted string does not exceed the maximum allowed
        @param value: string entered by user
        @param param_type: parameter type
        @param max_size: maximum size allowed for the string
        @return: entered string if it passes the length check
        @raise argparse.ArgumentTypeError: string length exceeds limit
        """
    if len(value) > max_size:
        raise argparse.ArgumentTypeError(
            f"{param_type} is greater than allowed string size: {value}")
    return value


def validate_date(date: str) -> str:
    """Validates that the date is in the correct format
    @param date: date provided by the user
    @return: valid date
    @raise argparse.ArgumentTypeError: Invalid date format
    """
    try:
        return str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date - format YYYY-MM-DD: {date}")


def validate_guid(value: str) -> str:
    """Validates that the user inputted string follows the GUID string standard
        @param value: user entered GUID
        @return: entered string if it passes regex check
        @raise argparse.ArgumentTypeError: Invalid guid format
        """

    if not bool(re.match("^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$", str(value))):
        raise argparse.ArgumentTypeError(
            f"GUID should be 36 characters displayed in five groups in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX. Hexdigits are not allowed.")

    return value

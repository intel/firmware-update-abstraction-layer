"""Parser class to parse the system argument

   Copyright (C) 2022-2023 Intel Corporation
   SPDX-License-Identifier: Apache-2.0
"""
import logging
import argparse

from typing import Any, Optional, Sequence
from .validator import validate_date, validate_string_less_than_n_characters, validate_guid

logger = logging.getLogger(__name__)

PATH_STRING = "Path"


class ArgsParser(object):
    """Parser class to parse command line parameter."""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description='Firmware Update Abstraction Layer Command-line tool to trigger updates')
        self.subparsers = self.parser.add_subparsers(
            help='valid commands: [fw, query]')

        self._parse_fw_args()
        self._parse_query_args()

    def parse_args(self, args: Optional[Sequence[str]]) -> Any:
        """Gets parsed arguments from user input.

        @param args: parameter entered by user
        """
        return self.parser.parse_args(args)

    @staticmethod
    def _add_source_options(parser: argparse.ArgumentParser):
        source_group = parser.add_mutually_exclusive_group(required=True)
        source_group.add_argument('--path', '-p', help='Full path to the update package',
                                  type=lambda x: validate_string_less_than_n_characters(x, PATH_STRING, 300))

    def _parse_query_args(self) -> None:
        parser = self.subparsers.add_parser('query')
        parser.add_argument('--option', '-o', default='all', required=False, type=str,
                            choices=['all', 'hw', 'fw'],
                            help='Type of information [all | hw | fw ]')
        parser.add_argument('--debug', '-d', required=False, help='Set log level to DEBUG', action='store_true')
        parser.set_defaults(func=_query)

    def _parse_fw_args(self) -> None:
        """Method to parse FW arguments"""
        # Create the parser for the "fw" command
        parser = self.subparsers.add_parser('fw')
        ArgsParser._add_source_options(parser)

        parser.add_argument('--releasedate', '-r', default='2024-12-31', required=False, type=validate_date,
                            help='Release date of the applying package - format YYYY-MM-DD')
        parser.add_argument('--vendor', '-v', default='Intel', required=False, help='Platform vendor',
                            type=lambda x: validate_string_less_than_n_characters(x, 'Vendor', 50))
        parser.add_argument('--biosversion', '-b', default='5.12', required=False, help='Platform BIOS version',
                            type=lambda x: validate_string_less_than_n_characters(x, 'BIOS Version', 50))
        parser.add_argument('--manufacturer', '-m', default='intel', required=False, help='Platform manufacturer',
                            type=lambda x: validate_string_less_than_n_characters(x, 'Manufacturer', 50))
        parser.add_argument('--product', '-pr', default='kmb-hddl2', required=False, help='Platform product name',
                            type=lambda x: validate_string_less_than_n_characters(x, 'Product', 50))
        parser.add_argument('--tooloptions', '-to', required=False, help='Firmware tool options',
                            type=lambda x: validate_string_less_than_n_characters(x, 'Tool Options', 10))
        parser.add_argument('--guid', '-gu', required=False, help='Firmware guid update',
                            type=lambda x: validate_guid(x))
        parser.add_argument('--autofill', '-af', required=False,
                            help='Autofill capsule information with platform information',
                            action='store_true')
        parser.add_argument('--debug', '-d', required=False, help='Set log level to DEBUG', action='store_true')

        parser.set_defaults(func=_fw)


def _fw(args) -> argparse.Namespace:
    """Sends arguments

    @param args: Arguments provided by the user from command line
    @return: User argument namespace
    """
    return args


def _query(args) -> argparse.Namespace:
    """Sends arguments

    @param args: Arguments provided by the user from command line
    @return: User argument namespace
    """
    return args

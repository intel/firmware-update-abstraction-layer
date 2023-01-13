"""Command-line Firmware Update Abstraction Layer tool to invoke Firmware Update Abstraction Layer Library.

Copyright (C) 2022-2023 Intel Corporation
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import logging
import sys

from falc.parser import ArgsParser
from falc.falc_exception import FalcException
from falc.command_factory import create_command_factory


logger = logging.getLogger(__name__)


class Falc(object):
    """Initialize the command-line tool.
    @param parsed_args: arguments from the user
    @param cmd_type: command type from the user
    """

    def __init__(self, parsed_args: argparse.Namespace, cmd_type: str) -> None:
        log_format = '%(levelname)s:%(message)s'
        if parsed_args.debug:
            logging.basicConfig(format=log_format, level=logging.DEBUG)
            logger.debug("Log level set to DEBUG")
        else:
            logging.basicConfig(format=log_format, level=logging.INFO)

        logger.info("Firmware Update Abstraction Layer command-line tool")

        self._command = create_command_factory(cmd_type)
        return_code = self._command.trigger_command(parsed_args)
        logger.debug(f'exit code={return_code}')
        sys.exit(return_code)


if __name__ == "__main__":  # pragma: no cover
    args_parse = ArgsParser()
    args = args_parse.parse_args(sys.argv[1:])
    if not len(vars(args)):
        args = args_parse.parse_args(["None"])
    try:
        Falc(args, sys.argv[1])
    except FalcException as error:
        logging.error(error)
        sys.exit(1)

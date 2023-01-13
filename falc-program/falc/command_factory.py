"""
    Factory to create the correct Command object

    # Copyright (C) 2022-2023 Intel Corporation
    # SPDX-License-Identifier: Apache-2.0
"""

from .falc_exception import FalcException
from .command import Command, FwCommand, QueryCommand
from .constant import QUERY, FW


def create_command_factory(cmd: str) -> Command:
    """Creates the concrete command class matching the command given by the user

    @param cmd: command string from user
    @return Concrete command object
    """
    if cmd == FW:
        return FwCommand()
    if cmd == QUERY:
        return QueryCommand()

    raise FalcException(f"Unsupported command {cmd}")

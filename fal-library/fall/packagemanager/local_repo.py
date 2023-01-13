"""
    On-disk implementation of Repo with simple add, get, list, exists
    functions

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

import logging
import os
from typing import List

from ..utility.file_handler import get_canonical_representation_of_path

from .irepo import IRepo
from ..fall_error import FallError

logger = logging.getLogger(__name__)


class DirectoryRepo(IRepo):  # pragma: no cover
    """On-disk implementation of Repo

    @param directory: Directory to use when creating repo
    """

    def __init__(self, directory: str) -> None:
        logger.debug("")
        self.__directory = get_canonical_representation_of_path(directory)

    def get_repo_path(self) -> str:
        """Gets the repository path

        @return: directory path
        """
        return self.__directory

    def get(self, filename: str) -> bytes:
        """Get file contents

        @param filename: filename of the source
        @return: contents of the file
        """
        with open(os.path.join(self.__directory, filename), 'rb') as f:
            contents: bytes = f.read()
        try:
            # the following line will be optimized out in byte code
            # and only used in unit testing
            assert isinstance(contents, bytes)  # noqa: S101
        except AssertionError:
            raise FallError('Filed opened contains strings instead of bytes')

        return contents

    def list(self) -> List:
        """List repo entries

        @return: list of files in the repository
        """
        return os.listdir(self.__directory)

    def exists(self) -> bool:
        """True if directory exists; false otherwise"""
        return os.path.isdir(self.__directory)

    def name(self) -> str:
        """Return repo path"""
        return self.__directory

    def is_present(self, name: str) -> bool:
        """Checks if filename exists in the repo

        @param name: name of the path to check
        @return: returns True if it exists or False if not.
        """
        return os.path.exists(os.path.join(self.__directory, name))

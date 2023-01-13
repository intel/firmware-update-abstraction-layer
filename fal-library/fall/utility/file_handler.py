"""
    Utility methods used in the project

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import os
import logging
import pathlib
import shutil

from typing import Union

logger = logging.getLogger(__name__)


def log_error(error: Exception) -> None:
    """Logs an error with the provided string

    @param error: Exception
    """
    logger.error(f"ERROR: {error}")


def get_canonical_representation_of_path(path: str) -> str:
    """Returns the canonical absolute expanded path of the path provided

    @param path: path
    @return canonical representation of the path
    """
    return os.path.normcase(
        os.path.normpath(
            os.path.realpath(
                os.path.abspath(
                    os.path.expanduser(path)
                )
            )
        )
    )


def check_path(path: Union[str, pathlib.Path]) -> None:
    logger.debug(f"check path: src:{path}")
    if not os.path.isfile(path):
        logger.debug(f"File does not exist or file path is not to a file: {path}")
        raise IOError("File does not exist or file path is not to a file.")

    if os.path.islink(path):
        logger.debug(f"Security error: Source file is a symlink: {path}")
        raise IOError("Security error: Source file is a symlink.")


def read_file(path: str, not_found_default: str) -> str:
    """Checks if the path exists.  If it does, it will read the specified line in the
    path.

    @param path: path
    @param not_found_default: default value to use if path is not found.
    @return: value associated with the specified path.
    """
    if not os.path.exists(path):
        return not_found_default

    try:
        with open(get_canonical_representation_of_path(path)) as f:
            return f.readline().rstrip('\n').split('\x00')[0]
    except OSError as e:
        raise ValueError(f'{e} Error while reading the file {path}')


def is_path_exist(path: str) -> bool:
    """Verifies to see if path exists or not

    @return: True if path exists; otherwise, false.
    """
    return True if os.path.isdir(path) else False


def move_file(source_file_path: str, destination_path: str) -> None:
    """ Move a file from one location to another using the same name.  This does not allow symlinks for
    either src or destination for security reasons.

    @param source_file_path: path of source file
    @param destination_path: path to destination file
    @raises: Symlink for src or destination.  Any errors during move.
    """
    canonical_src_path = get_canonical_representation_of_path(source_file_path)
    canonical_target_path = get_canonical_representation_of_path(destination_path)

    try:
        _check_paths(canonical_src_path, canonical_target_path)
    except IOError as e:
        raise IOError(f"Error while moving file: {e}")

    try:
        shutil.move(canonical_src_path, canonical_target_path)
    except (shutil.SameFileError, PermissionError, IsADirectoryError, FileNotFoundError, OSError) as e:
        raise IOError(f"Error while moving file: {e}")


def _check_paths(src: str, destination: str) -> None:
    logger.debug(f"check paths: src:{src}, destination:{destination}")
    if not os.path.isfile(src):
        logger.debug(f"File does not exist or file path is not to a file: {src}")
        raise IOError("File does not exist or file path is not to a file.")

    if os.path.islink(src):
        logger.debug(f"Security error: Source file is a symlink: {src}")
        raise IOError("Security error: Source file is a symlink.")

    if os.path.islink(destination):
        logger.debug(f"Security error: Destination is a symlink: {src}")
        raise IOError("Security error: Destination  is a symlink")

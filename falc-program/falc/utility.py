"""
    Utilities

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import os
from typing import List

from fall.result_constants import Result

CACHE_MANAGEABILITY = '/var/cache/manageability/'


def get_canonical_representation_of_path(path: str) -> str:
    """Returns the canonical absolute expanded path of the path provided for both windows and linux
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


def search_keyword(payload: Result, words: List[Result]) -> bool:
    """Stop FALC after receiving expected response
    @param payload: received result
    @param words: expected keywords in the message
    @return: True if keyword found, False if keyword not found in message
    """
    for word in words:
        if payload == word:
            return True
    return False

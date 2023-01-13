"""
    Result Constants used throughout the firmware update

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import json


# Result object classes
class Result:

    __slots__ = ("status", "message", "json")

    def __init__(self, status: int = 0, message: str = "") -> None:
        """Result object containing a status code and message

        @param status: (int) Predefined status code
        @param message: (str) Result message"""
        self.status = status
        self.message = message
        self.json = json.dumps({
            "status": status,
            "message": str(message)
        })

    def __eq__(self, other: object) -> bool:
        return self.json == str(other)

    def __hash__(self) -> int:
        return self.json.__hash__()

    def __repr__(self) -> str:
        return self.json


INSTALL_SUCCESS = Result(200, "SUCCESSFUL INSTALL")
QUERY_SUCCESS = Result(200, "SUCCESSFUL QUERY")

INPUT_VALIDATION_FAILURE = Result(400, 'FIRMWARE INPUT VALIDATION FAILURE')
UNABLE_TO_GET_PLATFORM_INFO_FAILURE = \
    Result(404, 'UNABLE TO GET PLATFORM INFORMATION')
UNABLE_FIND_MATCHING_PLATFORM = \
    Result(404, 'UNABLE TO FIND MATCHING PLATFORM IN CONFIGURATION FILE')
UPGRADE_CHECK_FAILURE = \
    Result(412,
           'PRE-CHECK OF SYSTEM INFORMATION FAILED.  '
           'DOES NOT MEET CRITERIA FOR FIRMWARE UPGRADE')
INSTALL_FAILURE = Result(500, 'INSTALL FAILED')
REBOOT_FAILURE = Result(500, 'REBOOT FAILED')
UNSUPPORTED_OS_FAILURE = Result(501, 'UNSUPPORTED OS')

"""
    Determine Paths based on OS

    @copyright: Copyright 2022-2023 Intel Corporation All Rights Reserved.
    @license: SPDX-License-Identifier: Apache-2.0
"""

import platform
from pathlib import Path

if platform.system() == 'Windows':  # pragma: no cover
    C_COLON = Path("c:\\")
    FALL_PATH = C_COLON / 'intel-manageability' / 'fall'
    SHARE_PATH_PREFIX = FALL_PATH / 'usr' / 'share'
else:
    ROOT = Path('/')
    SHARE_PATH_PREFIX = ROOT / 'usr' / 'share' / 'fall'

"""
    Path prefixes based on Operating System type

    @copyright: Copyright 2022-2023 Intel Corporation All Rights Reserved.
    @license: SPDX-License-Identifier: Apache-2.0
"""

from pathlib import Path

ROOT = Path('/')
RAW_ETC = ROOT / 'etc'
BINARY_SEARCH_PATHS = [ROOT / 'bin',
                       ROOT / 'usr' / 'sbin',
                       ROOT / 'usr' / 'bin',
                       ROOT / 'sbin']

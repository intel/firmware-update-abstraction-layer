"""
    Interface for the package manager.  Manages directory housing the update package.

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""

from abc import ABC, abstractmethod
from typing import List


class IRepo(ABC):  # pragma: no cover
    """Abstract base class for repos."""

    @abstractmethod
    def get_repo_path(self) -> str:
        """Get a path or equivalent name for the Repo.

        @return: Path or equivalent name for the Repo.
        """
        pass

    @abstractmethod
    def get(self, filename: str) -> bytes:
        """Get file contents from Repo"""
        pass

    @abstractmethod
    def list(self) -> List[str]:
        """List Repo entries"""
        pass

    @abstractmethod
    def exists(self) -> bool:
        """True if the Repo exists (e.g., if it's a directory on a filesystem); False otherwise."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return repo ID"""
        pass

    @abstractmethod
    def is_present(self, filename: str) -> bool:
        """Returns True if entry exists else False"""
        pass

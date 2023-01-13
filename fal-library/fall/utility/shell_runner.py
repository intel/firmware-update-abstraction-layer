"""
    Runs shell commands

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import os
import shlex
import subprocess
import logging
from subprocess import Popen, PIPE

from typing import Tuple, Optional, Union, List, Any
from ..constants import AFULNX_64
from .path_prefixes import BINARY_SEARCH_PATHS

logger = logging.getLogger(__name__)


class PseudoShellRunner:
    """Required to run shell commands"""

    @staticmethod
    # should be Popen[bytes] but not yet supported in this Python version
    def get_process(cmd: Union[str, List[str]]) -> Any:
        """Returns a shell to process a command

        @param cmd: command to execute
        """
        return Popen(cmd, shell=False, stdout=PIPE, preexec_fn=os.setsid)

    @classmethod
    def _sanitize(cls, filename: str) -> str:
        """Remove unsafe characters from string filename and return result

        @param filename: name of the file to save logs
        """
        return filename.replace(" ", "_").replace("/", "_")

    @classmethod
    def run(cls, cmd: str, cwd: Optional[str] = None) \
            -> Tuple[str, Optional[str], int]:
        """Run/Invoke system commands

        @param cmd: Shell cmd to execute
        @param cwd: if not None, run process from this working directory
        @return: Subprocess result (output, error (possibly None) & exit status)
        """
        shlex_split_cmd = cls.interpret_shell_like_command(cmd)

        logger.debug(
            "run calling subprocess.Popen " +
            str(shlex_split_cmd) +
            " with cwd " + str(cwd))

        proc = subprocess.Popen(
            shlex_split_cmd,
            cwd=cwd,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        (out, err) = proc.communicate(b'yes\n') if AFULNX_64 in cmd \
            else proc.communicate()

        # we filter out bad characters but still accept the rest of the string
        # here based on experience running the underlying command

        decoded_out = out.decode('utf-8', errors='replace')
        decoded_err = None if err is None else err.decode('utf-8', errors='replace')
        return decoded_out, decoded_err, proc.returncode

    @classmethod
    def interpret_shell_like_command(cls, cmd: str) -> List[str]:
        """Take a command intended for a shell and perform minimal
        transformation to allow it to run with shell=False.  Command
        will be split with quoting support and if the command can be found
        in common POSIX locations such as /bin, it will be expanded.

        @param cmd: string with command and arguments
        @return: array suitable for Popen with shell=False
        """

        def which(program):
            import os

            def is_exe(fpath):
                return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

            fpath, fname = os.path.split(program)
            if fpath:
                if is_exe(program):
                    return program
            else:
                extension = ""

                for path in BINARY_SEARCH_PATHS:
                    exe_file = os.path.join(path, program + extension)
                    if is_exe(exe_file):
                        return exe_file

            return None

        shlex_split_cmd = shlex.split(str(cmd))
        which_cmd = which(shlex_split_cmd[0])
        if which_cmd:
            shlex_split_cmd[0] = which_cmd
        return shlex_split_cmd

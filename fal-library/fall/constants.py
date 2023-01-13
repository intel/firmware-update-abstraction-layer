"""
    Constants used by the platform firmware update tool.
    @copyright: Copyright 2022-2023 Intel Corporation All Rights Reserved.
    @license: SPDX-License-Identifier: Apache-2.0
"""
UNKNOWN = 'Unknown'

# Afulnx tool name
AFULNX_64 = 'afulnx_64'


# Package types
PACKAGE = 'package'
BIOS = 'bios'
CERT = 'cert'

# Command prefix to run a command 'as the host' using docker, chroot, and namespace control
# note this will not propagate proxy environment variables
# change above comment if -e entries are added for proxies
DOCKER_CHROOT_PREFIX = "/usr/bin/docker run -e DEBIAN_FRONTEND=noninteractive --privileged --rm --net=host --pid=host -v /:/host ubuntu:20.04 /usr/sbin/chroot /host "

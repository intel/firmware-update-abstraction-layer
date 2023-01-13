# Copyright (c) 2022-2023 Intel Corporation
# SPDX-License-Identifier: Apache 2.0

FROM ubuntu:22.04

RUN apt-get update && apt-get -yq install lsb-release less && apt-get clean
COPY reboot /sbin/reboot
RUN chmod +x /sbin/reboot
COPY falc-program.deb /install/falc-program.deb
COPY install-fal.sh /install/install-fal.sh
RUN chmod +x /install/install-fal.sh && /install/install-fal.sh
COPY bios/capsule.bio /bios/capsule.bio

CMD ["/usr/bin/falc", "fw", "--autofill", "-p", "/bios/capsule.bio"]

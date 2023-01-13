#!/bin/bash
set -eo pipefail
# Shell script that installs Firm
# Usage:
#   Run: sudo ./install-falc.sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Failed checks will terminate the script with a message to operator.
# Ensure we're running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Ensure we're running a supported OS
verified_os_list=("Ubuntu 20.04" "Ubuntu 22.04")

if [[ ${verified_os_list[@]} == *"$(lsb_release -rs)"* ]]; then
  OS_TYPE="Ubuntu-$(lsb_release -rs)"
  echo "Confirmed Supported Platform (Ubuntu $(lsb_release -rs))"
elif [ "$(lsb_release -sc)" == "buster" ] | [ "$(lsb_release -sc)" == "bullseye" ] ; then
  OS_TYPE="Debian"
  echo "Confirmed Supported Platform (Debian $(lsb_release -sc))"
else
  echo "WARNING: Unverified OS version detected. Recommend use of verified OS versions: ${verified_os_list[@]}"
fi

# Use script directory as installation directory
INST_DIR="$DIR"

# Ensure installation packages are present
if [[ $(ls "$INST_DIR" | grep ".deb" | wc -l) -eq 0 ]]; then
    echo "Installation packages not found. Exiting."
    exit 1
fi

# install FALC
echo "Will install FALC executable"

dpkg -i "$DIR"/falc*.deb

echo "Firmware Update Abstraction Layer (FAL) Installation Complete"
exit 0

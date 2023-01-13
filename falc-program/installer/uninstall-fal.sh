#!/bin/bash

set -eo pipefail

function uninstall {
  # Ensure we're running as root
  if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
  fi

  if dpkg -l | grep falc; then
    uninstall_falc
  fi
}

function uninstall_falc {
  echo Uninstalling Firmware Update Abstraction Layer Command-line Tool '(falc)'...
  dpkg --purge falc-program
  rm -rf /usr/share/fall
  return 0
}

uninstall

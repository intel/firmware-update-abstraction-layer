#!/bin/bash
set -e

. ./integration-messages.sh

suite_started "Prepare tests"
launchers/vagrant-up.sh
suite_finished "Prepare tests"

launchers/test-install-uninstall.sh
launchers/fw_update.sh

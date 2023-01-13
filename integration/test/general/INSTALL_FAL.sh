#!/bin/bash

set -euxo pipefail

cd /vagrant/input
chmod +x *.sh
bash -x ./install-fal.sh

# now check if falc can be run in help mode
falc -h

bash -x ./uninstall-fal.sh
# check that falc is gone
! [ -f /usr/bin/falc ]

# reinstall
bash -x ./install-fal.sh

# check falc again
falc -h

# make a backup of systemctl for manual use after running tests
cp /usr/bin/systemctl /usr/bin/systemctl.bak

#!/bin/bash
set -e

apparmor_reload() {
	source /etc/os-release
	if [ "$ID" = "ubuntu" ]; then
	    apparmor_parser -r -W -T $1
	else
	    systemctl restart apparmor
	fi
}

SYSTEMD_DIR=/lib/systemd/system

echo "After install called"

if [ "$(cat /proc/1/comm)" == "systemd" ]; then
	echo "Found systemd"
	echo "Activating FALC apparmor policies"
	apparmor_reload /etc/apparmor.d/usr.bin.falc
	# Reload daemon to pick up new changes
	systemctl daemon-reload
	echo "Ran systemctl daemon-reload"
else
	echo "No systemd found; skipping AppArmor reload"
fi

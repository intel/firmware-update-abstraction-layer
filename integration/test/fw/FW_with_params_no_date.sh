#!/bin/bash

set -euxo pipefail

# Test that FALC is calling the bios update script.

# Make a custom firmware entry that will match integration reloaded VM.
cat >/usr/share/fall/firmware_info.db <<EOF1
<?xml version="1.0" encoding="utf-8"?>
<firmware_component>
    <firmware_product name='Standard PC (i440FX + PIIX, 1996)'>
        <bios_vendor>QEMU</bios_vendor>
        <operating_system>linux</operating_system>
        <firmware_tool>TestUpdateBIOS.sh</firmware_tool>
        <firmware_file_type>bio</firmware_file_type>
    </firmware_product>
</firmware_component>
EOF1

# Make a BIOS update script that will write its argument to a path in /tmp
cat >/usr/bin/TestUpdateBIOS.sh <<EOF2
#!/bin/bash
set -ex
echo "Test bios updater running."
echo \$1 >/tmp/test_bios_updater
EOF2
chmod +x /usr/bin/TestUpdateBIOS.sh

# Remove files from any previous runs
rm -f /tmp/test_bios_updater

# Set up fake bios file
rm -f /tmp/fw.bio
touch /tmp/fw.bio

# Set up fake reboot script
rm -f /tmp/rebooted
cat >/sbin/reboot <<EOF3
#!/bin/bash
set -ex
echo "Fake rebooter."
echo reboot >/tmp/rebooted
EOF3

falc fw --debug --path /tmp/fw.bio --product "Standard PC (i440FX + PIIX, 1996)" --vendor SeaBIOS --manufacturer QEMU

grep /tmp/fw.bio /tmp/test_bios_updater
[ -f /tmp/rebooted ]

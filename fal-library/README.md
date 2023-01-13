# Platform Firmware Updater Library (Python)

The objective of the Platform Firmware Updater is to provide an easily integrated mechanism to perform FW/BIOS updates on Edge devices.  It is written as a Python library.

<details>
<summary>Table of Contents</summary>

1. [Features](#features)
2. [APIs](#apis)
   1. [Update Firmware](#update-firmware)
   2. [Query](#query)
3. [Firmware Updates](#firmware-updates)
4. [Extending Firmware Support](#extending-firmware-support)
   1. [Understanding Firmware Database File](#understanding-firmware-database-file)
   2. [Firmware Database Parameter Values](#firmware-database-parameter-values)
5. [Build Instructions](#build-instructions)
   1. [How to Build](#how-to-build)
   2. [Build Output](#build-output)
6. [Install Library](#install-library)
    1. [Database File Setup](#database-file-setup)
7. [Run Unit Tests](#run-unit-tests)

</details>


## Features

| Features                      | Description                                                                          |
|:------------------------------|:-------------------------------------------------------------------------------------|
| Update Firmware on the system | Provides a native and containerized solution to update the firmware on any platform. |
| Query system information      | Provides a way to get the hardware and firmware information on the system.           |

## APIs

There are 2 APIs to the Firmware Update Abstraction Layer library (FALL).  The APIs are located in the firmware_updater.py file

### Update Firmware

**Method Name:** ```Update```

| Parameter              |     Type      | Default      | Required/<br>/>Optional | Description                                                                                                                                                                    |
|:-----------------------|:-------------:|:-------------|:-----------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| path_to_update_package |      str      | N/A          |        required         | Path to the update file                                                                                                                                                        |
| capsule_release_date   | Optional[str] | current date |        optional         | Release date of the capsule.  To be verified with the date on the platform to determine if the update is needed                                                                |
| bios_vendor            | Optional[str] | None         |        optional         | BIOS vendor name.  This will be compared with the vendor on the system to ensure there is a match prior to the update.  **REQUIRED if autofill_platform_info == False**        | 
| platform_name          | Optional[str] | None         |        optional         | Platform name.  This will be used to find a match with the database file to determine how to update the system.  **REQUIRED if autofill_platform_info == False**               |
| platform_manufacturer  | Optional[str] | None         |        optional         | Platform manufacturer.  This will be compared with the manufacturer on the system to ensure there is a match prior to the update.  **REQUIRED if auto_platform_info == False** |
| hash_algorithm         | Optional[int] | None         |        optional         | Currently this is not being used.                                                                                                                                              |
| autofill_platform_info |     bool      | False        |        required         | If set to True, then the capsule information will automatically be made to match what is on the system.  If set to false, the user needs to fill in those parameters.          |


### Query

Returns the hardware and firmware information on the system.  

**Method Name:** ```Query```


| Parameter              |     Type      | Default | Required/Optional | Description                                                                    |
|:-----------------------|:-------------:|:--------|:-----------------:|:-------------------------------------------------------------------------------|
| option_type            |      str      | 'all'   |     optional      | Information to return about the system.  See link below for option information |

#### Option Results
[Allowed Options and Results](https://github.com/intel-sandbox/PFU/tree/develop/doc/query.md)

## Firmware Updates

To perform Firmware updates, IBVs must supply the SMBIOS or Device Tree info
that is unique to each platform SKU. The info must fulfill the vendor,
release date, manufacturer, and product name that matches the
endpoint as shown below.

Prior to sending the manifest the user needs to make sure that the
platform information is present within the
```/usr/share/firmware_info.db`` file. Refer to [Extending FW Support](#extending-firmware-support) on how to modify the file and extend firmware support to a new platform.

The following information must match the data sent in the firmware update command for Platform Firmware Updater to initiate a firmware update.

| Information | Field        | Checks                                                    |
|:------------|:-------------|:----------------------------------------------------------|
| Firmware    | Vendor       | Exact string match                                        |
|             | Release Date | Checks if the firmware capsule date is newer than current |
| System      | Manufacturer | Exact string match                                        |
|             | Product Name | Exact string match                                        |

To find the firmware and system  information, either use the Query API on the library or run the commands
below:

**Intel x86 UEFI-based products**

For UEFI based platforms, the firmware and system information can be found running the following command:

```shell
dmidecode –t bios –t system
```

## Extending Firmware Support
The Platform Firmware Updater Library supports a scalable Firmware solution where triggering a firmware update on any new platform is made easy by adding the platform
related information to a config file that the library uses while installing the new firmware.

### Understanding Firmware Database File 
The Firmware database is located at ```/usr/share/firmware_info.db```.
This file consists of all the platform information required to perform the firmware update.

If a new platform needs to be supported, the user needs to add the platform related information in the XML format within this
database file.

The XML format of the database file looks similar as the following snippet:
```xml
<?xml version="1.0" encoding="utf-8"?>
<firmware_component>
    <firmware_product name='NUC6CAYS'>
        <bios_vendor>Intel Corp.</bios_vendor>
        <operating_system>linux</operating_system>
        <firmware_tool>UpdateBIOS.sh</firmware_tool>
        <firmware_file_type>bio</firmware_file_type>
    </firmware_product>
</firmware_component>
```
Once the platform information is added, there are no code changes required. This information from the database XML file will be used by the code
to perform a firmware update.

### Firmware Database Parameter Values

The following table helps in understanding what each tag in the firmware database file refers to. The **Required(R)/Optional(O)** field
associated with each tag represents whether the tag is mandatory or not while adding a new platform information.

| Tag                                                     | Attributes           | Example                                                            | Required/Optional | Notes                                                                                                                                                                                              |
|:--------------------------------------------------------|:---------------------|:-------------------------------------------------------------------|:-----------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<?xml version='1.0' encoding='utf-8'?>`                |                      |                                                                    |         R         |
| `<firmware_component>`                                  |                      | `<firmware_component>`                                             |         R         ||
| `<firmware_product>`                                    |                      | See examples below with attributes                                 |         R         | Use the latter when tool_options is required by the firmware bootloader to install the FW.  This is the platform name. Run the command ‘***dmidecode –t bios –t system***’ to view the information |
|                                                         | name=PLATFORM_NAME   | `<firmware_product name='NUC6CAYS'>  `                             |         R         |                                                                                                                                                                                                    |
|                                                         | guid=[true or false] | `<firmware_product name='Alder Lake Client Platform' guid='true'>` |         O         |                                                                                                                                                                                                    |
| `<operating_system></operating_system>`                 |                      | `<operating_system>linux</operating_system>`                       |         R         | OS name – [linux or windows]  Currently only linux is supported.                                                                                                                                   |
| `<firmware_file_type></firmware_file_type>`             |                      | `<firmware_file_type>bio</firmware_file_type>`                     |         R         | FW file type – bio, fv, cap etc.                                                                                                                                                                   |
| `<bios_vendor></bios_vendor>`                           |                      | `<bios_vendor>Intel Corp.</bios_vendor>`                           |         O         | Run the command '***dmidecode –t bios –t system***’ to view the information                                                                                                                        |
| `<firmware_tool></firmware_tool>`                       |                      | `<firmware_tool>UpdateBIOS.sh</firmware_tool>`                     |         O         | FW tool used for update.  Can be obtained from the vendor                                                                                                                                          |
| `<manufacturer></manufacturer>`                         |                      | `<manufacturer>Intel Corp.</manufacturer>`                         |         O         | Run the command ‘***dmidecode –t bios –t system***’ to view the information                                                                                                                        |
| `<firmware_dest_path><firmware_dest_path>`              |                      | `<firmware_dest_path>/boot/efi/</firmware_dest_path>`              |         O         | Location to store new FW file.  Only used on the platforms where the FW update is just to replace the existing firmware file in a path.                                                            |
| `<firmware_tool_args></firmware_tool_args>`             |                      | `<firmware_tool_args>--apply</firmware_tool_args>`                 |         O         | Additional arguments that follow the firmware tool command to apply firmware                                                                                                                       |
| `<firmware_tool_check_args></firmware_tool_check_args>` |                      | `<firmware_tool_check_args>-s</firmware_tool_check_args>`          |         O         | Additional arguments to check if a FW tool exists on system.                                                                                                                                       |
| `<tool_options></tool_options>`                         |                      | `<tool_options>-p -b</tool_options>`                               |         O         | Extra parameters required to use the tool                                                                                                                                                          |
| `</firmware_product>`                                   |                      | `</firmware_product>`                                              |         R         |                                                                                                                                                                                                    |                                                                                                                                                       |
| `</firmware_component>`                                 |                      | `</firmware_component>`                                            |         R         |                                                                                                                                                                                                    |


## Build Instructions

### How to build
* Prepare a Linux machine with Docker installed.  Ensure the 'm4' and 'bash' packages are also installed (these are available in all major Linux distributions).
* If you are behind a proxy, ensure your http_proxy, https_proxy, and no_proxy variables are set correctly and exported.  E.g., in bash, you could run: "http_proxy=http://foo.com:1234/ && export http_proxy"
* Optional but recommended for better build speed and caching: export DOCKER_BUILDKIT=1
* Run: ./build.sh

If you see something like 'unable to resolve' or a DNS error or 'unable to look up' near the start of the build, follow the instructions under https://docs.docker.com/install/linux/linux-postinstall/ --> "DISABLE DNSMASQ".  This can occur in some Linux distributions that put 127.0.0.1 in /etc/resolv.conf.

### Build output
* When build is complete, a ```fall-*.whl``` file will be in the `dist` folder.  This is the library.

## Install Library

The library can be installed on the system using the generated wheel file.  The library is not located on a PyPi repository, so it either needs to be installed using the code itself or the wheel file.

1. Install using the code (at the pfu-library root directory)
    - ```pip3 install .``` 
2. Install using the wheel file
    - ```pip3 install fall*.whl```

### Database File Setup

❗ The database and schema files need to be placed in the correct directories.

1. ```fal-library/firmware_db_schema.xsd``` file needs to be in the ```/usr/share/fall``` folder.
2. ```fal-library/firmware_info.db``` file needs to be in the ```/usr/share/fall``` folder.
3. The platform information needs to be added to the firmware_info.db file in order for the update to be successful.


## Run Unit Tests

- Install Python 3.10
- Install requirements: ```pip3 install -r requirements.txt```
- Run: `make tests`

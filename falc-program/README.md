# Firmware Update Abstraction Layer Command-Line (FALC) Tool

<details>
<summary>Table of Contents</summary>

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Notes](#-notes)
4. [Commands](#commands)
   1. [FW](#fw)
   2. [Query](#query)
5. [Status Codes](#status-codes)
6. [Return and Exit Codes](#return-and-exit-codes)
7. [FAQ](#-faq)
   1. [How do I find what values to use for FW update?](#-how-do-i-find-what-values-to-use-for-a-fw-update)
      

</details>

# Introduction

This is reference code to demonstrate how the Firmware Update Abstraction Layer Library (FALL) may be used to update the FW on a device.

# Prerequisites
This tool requires the Firmware Update Abstraction Layer Library (FALL) to be installed.  

# 📝 Notes
1. Use the query command to find system information needed to fill in FW update parameters.
2. If placing files local on the system for update, they need to be placed in a folder with read/write access in the apparmor profile.  The recommended path would be ```/var/cache/manageability```.  If another directory is used, the apparmor profile would need to
be modified to allow read/write access to that directory.
3. The `-d` parameter can be set to enable debug logging.


# Commands

## FW
### Description
Performs a Firmware update on an Edge Device.

❗ See [Note #2](#-notes) if placing files local on the system.

### Usage
```
falc fw {--path,  -p=PATH}  
   [--releasedate, -r RELEASE_DATE; default="2024-12-31"] 
   [--vendor, -v VENDOR; default="Intel"] 
   [--manufacturer, -m MANUFACTURER; default="intel"] 
   [--product, -pr PRODUCT; default="kmb-hddl2"] 
   [--tooloptions, -to TOOL_OPTIONS]
   [--guid, -g GUID]
   [--autofill, -af]
   [--debug, -d]
```

### Examples

#### FW Update - automatically make capsule information match platform information
```
falc fw -p <local path to FIP>/fip-hddl2.bio --autofill
 ```
#### FW Update - provide capsule informationIntel Corp.
```
falc fw -p <local path to FIP>/fip-hddl2.bin 
   --releasedate 2022-11-3
   --product NUC8i3BEH
   --vendor Intel
 ```


## QUERY
### Description
Query device for attributes

### Usage
```
falc query [--option, -o=[all | hw | fw ]; default='all'] [--debug, -d]  
```

### Option Results
[Allowed Options and Results](https://github.com/intel-sandbox/PFU/tree/develop/docs/query.md)


### Examples
#### Return all attributes
```
falc query
```
#### Return only 'hw' attributes
```
falc query --option hw
```
#### Return only 'sw' attributes
```
falc query --option sw
```

# Status Codes

 | Message         | Description                           | Result                                        |
|:----------------|:--------------------------------------|:----------------------------------------------|
| COMMAND_SUCCESS | Post and pre-install check go through | {'status': 200, 'message': 'COMMAND SUCCESS'} |
| FILE_NOT_FOUND  | File to be fetched is not found       | {'status': 404, 'message': 'FILE NOT FOUND'}  |
 | COMMAND_FAILURE | Update did not go through             | {'status': 400, 'message': 'COMMAND FAILURE'} |

# Return and Exit Codes

| Return Code | Exit Code | Description       |
|:-----------:|:---------:|:------------------|
|      0      |     0     | SUCCESS           |
|      1      |     1     | FAIL              |


# ❔ FAQ

<details><summary>[See answers to frequently asked questions]</summary>

### ❓ How do I find what values to use for a FW update?

> Use the query command with the '--option all' flag


</details>

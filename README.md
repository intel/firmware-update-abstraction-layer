# Firmware Update Abstraction Layer (FAL)

The Firmware Update Abstraction Layer (FAL) is a combination of the following to provide a firmware update solution that can be used to perform FW/BIOS updates across a heterogeneous mix of edge systems.

## Supported OS
* Ubuntu

## Components

There are 3 Components to the Firmware Update Abstraction Layer (FAL).  The main deliverable of this project is the Firmware Update Abstraction Layer Library (FALL).  The other two components are reference code to demonstrate how the library may be used.

See the individual README.md files for more information on each component.

| Component                                      | Acronym | Description                                                                                                                     |
|:-----------------------------------------------|:--------|:--------------------------------------------------------------------------------------------------------------------------------|
| Firmware Update Abstraction Library            | FALL    | Python library that performs the update                                                                                         |
| Firmware Update Abstraction Layer Command-Line | FALC    | Reference code which utilizes the FALL.  It can be used to test the library or as a reference for developing your own solution. |             |
| Dockerfile                                     |         | Reference Dockerfile on how the solution could be containerized                                                                 |

# Documentation

PFU Library [Readme](fal-library/README.md)

PFU Command-line [Readme](falc-program/README.md)

Running in a [Docker container](docker/README.md)

Please also see [the docs directory](docs).

## Build

### Prerequisites
* install m4 

`sudo apt install m4`

* install Docker
```
sudo apt-get -y install curl 
# install docker using the convenience script 
curl -fsSL https://get.docker.com -o get-docker.sh 
# preview script steps before running 
DRY_RUN=1 sh ./get-docker.sh 
sudo sh get-docker.sh![image](https://github.com/intel-sandbox/PFU/assets/13474711/9b5b7ab0-f0a0-4fd1-99f9-92970795d7d6)
```

### Build Project
`./build.sh`

See the docker subdirectory for instructions on building a Docker image.

## Install (Native using reference code):

* Change directory: `cd falc-program/installer`
* Run script: `./install-fal.sh`


## Uninstall (Native using reference code):

* Change directory: `cd falc-program/installer`
* Run script: `./uninstall-fal.sh`
 

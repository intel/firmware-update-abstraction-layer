# Introduction

integration is sub-project within FALC which helps create an Ubuntu VM for integration testing

# Local setup

## Prerequisites:
Installing Vagrant, Vagrant-libvirt, Qmenu-KVM and the plugins etc

1. Download vagrant from vagrant https://www.vagrantup.com/downloads.html and
  install by `dpkg -i <yourvagrantdownload>.deb`

2. Edit the /etc/apt/sources.list and uncomment all the deb-src lines

3. Run the below commands in sequence (preferably as root)
``` 
    apt update
    apt install qemu qemu-kvm libvirt-bin
    apt-get build-dep vagrant ruby-libvirt
    apt-get install qemu libvirt-bin ebtables dnsmasq
    apt-get install libxslt-dev libvirt-dev zlib1g-dev ruby-dev
```

1. Install the vagrant plugins:
```
vagrant plugin install vagrant-share
vagrant plugin install vagrant-libvirt
```

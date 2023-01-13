To build a Docker container that will update an Intel NUC:

1. Put `capsule.bio` in the `bios` subdirectory
2. Ensure you can run docker from your account. Test with `docker run hello-world`
3. Run `./build.sh` in this directory 
4. Setup the custom apparmor profile:

     a. copy falc-policy /etc/apparmor.d/containers/falc-policy
     
     b. load the profile: `sudo apparmor_parser -r -W /etc/apparmor.d/containers/falc-policy`
     
After the image is built, the following examples can be used as a starting point to run the update in a container:

1. system using the UpdateBIOS shell script such as a NUC:

```docker run --privileged --rm -v /usr/bin/UpdateBIOS.sh:/usr/bin/UpdateBIOS.sh:ro -v /sys:/sys:ro -v /boot:/boot:rw -v /proc:/proc:rw falc```

2. system using the fwupdate tool such as Alder Lake:

```sudo docker run --privileged --rm -v /usr/bin/fwupdate:/usr/bin/fwupdate:ro -v /lib:/lib:rw -v /sys:/sys:ro -v /boot:/boot:rw -v /run:/run:ro -v /usr/libexec:/usr/libexec:rw -v /proc:/proc:rw --security-opt apparmor=falc-policy falc```

Alternately, if you want to run falc with custom command line arguments, you can use this command (substitute your own desired arguments):

```docker run --privileged --rm -v /usr/bin/UpdateBIOS.sh:/usr/bin/UpdateBIOS.sh:ro -v /sys:/sys:ro -v /boot:/boot:rw -v /proc:/proc:rw falc /usr/bin/falc fw -p /bios/capsule.bio -v "Intel Corp." -m "Intel(R) Client Systems" -pr "NUC7i3DNKTC" -b "DNKBLi30.86A.0070.2020.0924.1032"```

## Apparmor policy

A reference Apparmor policy is included in `falc-policy`. See https://docs.docker.com/engine/security/apparmor/ for information on how to customize this policy and attach it to your container.

#!/bin/bash
set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[ -f bios/capsule.bio ] || ( echo "Please put capsule.bio in the bios subdirectory." ; exit -1 )

cd "$DIR/.."
rm -rf dist
./build.sh

cd "$DIR"
ls ../dist
cp ../dist/falc-program*.deb falc-program.deb
cp ../dist/install-fal.sh install-fal.sh
cp ../dist/uninstall-fal.sh uninstall-fal.sh

docker build \
    --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
    --build-arg http_proxy=${http_proxy:-} \
    --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
    --build-arg https_proxy=${https_proxy:-} \
    --build-arg NO_PROXY=${NO_PROXY:-} \
    --build-arg no_proxy=${no_proxy:-} \
    -t falc \
    .

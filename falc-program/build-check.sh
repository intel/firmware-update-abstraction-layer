#!/bin/bash
set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Update version
cp -vf "$DIR"/version.txt "$DIR"/fpm-template/usr/share/falc/version.txt

"$DIR"/dockerfiles/build-Dockerfile.sh check

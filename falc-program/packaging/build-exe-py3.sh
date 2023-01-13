#!/bin/bash

set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

AGENT=$1
FORMAT=$2
TYPE=program

AGENTDIR="$AGENT-$TYPE"

rm -rf dist build fpm-files
mkdir -p dist
cp -r fpm-template fpm-files
mkdir -p fpm-files/usr/bin/

pwd
#Build and copy executable into DEB staging area
"$DIR"/run-pyinstaller-py3.sh "$AGENT-$TYPE" "$AGENT"
echo copying pyinstaller binary
cp -r ../"$AGENTDIR"/dist/"$AGENT" fpm-files/usr/bin/
chmod +x fpm-files/usr/bin/"$AGENT"

ITERATION=`cat iteration.txt`
NAME="$AGENT"-"$TYPE"
VERSION="$(cat ../version.txt)"

if [ -z "${BUILD_NUMBER+x}" ]; then
    ITERATION=${ITERATION}
else
    ITERATION=${BUILD_NUMBER}
fi

PACKAGE_NAME="$NAME-$VERSION-$ITERATION.$2"
fpm -t $2\
    --after-install scripts/after-install.sh\
    --before-install scripts/before-install.sh\
    --before-remove scripts/before-remove.sh\
    --iteration ${ITERATION}\
    -s dir\
    -C fpm-files\
    -p "$PACKAGE_NAME"\
    -f\
    -n ${NAME}\
    -v ${VERSION}\
    --no-auto-depends\
    -a all\
    -m none\
    .

mkdir -p dist/
mv -f "$PACKAGE_NAME" dist/


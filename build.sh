#!/bin/bash
set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR"
rm -rf "$DIR"/dist
mkdir -p "$DIR"/dist

"$DIR"/fal-library/build.sh
mkdir -p "$DIR"/dist
cp "$DIR"/fal-library/output/fall-*.whl "$DIR"/dist
cp "$DIR"/fal-library/output/fall-*.whl "$DIR"/falc-program/packaging

"$DIR"/falc-program/build.sh
cp "$DIR"/falc-program/output/*.deb "$DIR"/dist
cp "$DIR"/falc-program/output/*install*.sh "$DIR"/dist

rm "$DIR"/falc-program/packaging/fall-*.whl

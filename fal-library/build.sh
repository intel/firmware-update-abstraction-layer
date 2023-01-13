#!/bin/bash
set -euxo pipefail

DOCKER_CONTENT_TRUST=0
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

NAME=fall

perl -pi -e 'chomp if eof' "$DIR"/../version.txt

rm -rf "$DIR"/output

# Run all checks and all Python unit tests
./build-check.sh
rsync -av output-check/ output/
rm -rf output-check/

# Build main output for Linux
./build-main.sh
rsync -av output-main/ output/
rm -rf output-main/

cp -v ../LICENSE "$DIR"/output
cp -v ../third-party-programs.txt "$DIR"/output/fall-third-party-programs.txt

if [ -x tree ] ; then
    tree "$DIR"/output
fi

echo build.sh complete

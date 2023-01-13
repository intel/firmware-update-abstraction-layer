#!/bin/bash
set -exo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SOURCENAME="$1"
SOURCEDIR="$SOURCENAME"
DESTNAME="$2"

cd "$DIR"/..
if [ -f dist/"$DESTNAME" ] ; then
  echo "Pyinstaller binary for $DESTNAME already built. Exiting."
  echo "(remove falc-program/dist if you want to rebuild)"
  exit 0
fi

rm -rf dist
rm -rf build
PYFLAGS=""

rm -f setup.cfg

VIRTUAL_ENV="${VIRTUAL_ENV:-}"
if [ -d "$VIRTUAL_ENV" ] ; then
  source "$VIRTUAL_ENV"/bin/activate
  SKIP_PIP=1
else
  python3 -m venv env && source env/bin/activate || echo "venv failed; proceeding without a virtual environment"
  SKIP_PIP=0
fi

if [ "$SKIP_PIP" == "1" ]; then
    echo "Skipping pip3"
else
    pip3 install -r requirements.txt
fi

pyinstaller "$DESTNAME".spec
echo done with pyinstaller script

#!/bin/bash
set -e

PACKAGE_TYPE="$1"
PROJECT="$2"
packaging/build-exe-py3.sh falc "$PACKAGE_TYPE" "$PROJECT" program

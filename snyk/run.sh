#!/bin/bash
set -euxo pipefail

export DOCKER_BUILDKIT=1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#cd "$DIR/.."
#./build.sh # Build to get .whl file for scans
#cp dist/*.whl ./falc-program

cd "$DIR"

DOCKER_NAME=fal-snyk

docker build \
    --build-arg HTTP_PROXY=${HTTP_PROXY:-} \
    --build-arg http_proxy=${http_proxy:-} \
    --build-arg HTTPS_PROXY=${HTTPS_PROXY:-} \
    --build-arg https_proxy=${https_proxy:-} \
    --build-arg NO_PROXY=${NO_PROXY:-} \
    --build-arg no_proxy=${no_proxy:-} \
    --disable-content-trust \
    -t ${DOCKER_NAME} \
    -f "$DIR"/Dockerfile "$DIR"

export NO_PROXY=$NO_PROXY,snyk.devtools.intel.com

scan_python () {
    docker run -e HTTP_PROXY -e HTTPS_PROXY -e NO_PROXY -e SNYK_ORG -e SNYK_TOKEN -e SNYK_API -v $DIR/..:/repository "$DOCKER_NAME" bash -x /scan-python.sh "$@"
}

rm -rf "$DIR"/results
mkdir -p "$DIR"/results

for i in fal-library falc-program ; do
    scan_python /repository/$i $i >"$DIR"/results/snyk-$i.html
done

cat "$DIR"/results/snyk-*.html >"$DIR"/results/all-in-one-snyk.html

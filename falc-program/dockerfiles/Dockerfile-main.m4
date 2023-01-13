# base image with all dependencies for building
FROM registry.hub.docker.com/library/ubuntu:20.04 as base
include(`commands.base-setup.m4')

# build a virtual environment to build from

# py3 venv
FROM base as venv-py3
WORKDIR /
RUN python3.10 -m venv /venv-py3 && \
    source /venv-py3/bin/activate && \
    pip3.10 install --upgrade pip && \
    pip3.10 install teamcity-messages==1.28 virtualenv==20.16.3 wheel==0.37.1 -U
RUN source /venv-py3/bin/activate

# ---falc---

FROM venv-py3 as venv-falc-py3
COPY falc-program/requirements.txt /src/falc-program/requirements.txt
COPY falc-program/packaging /src/packaging
RUN cp -v /src/packaging/*.whl /src/falc-program
WORKDIR /src/falc-program
RUN source /venv-py3/bin/activate && \
    pip3.10 install -r requirements.txt
COPY falc-program/version.txt /src/version.txt
COPY falc-program /src/falc-program

FROM venv-falc-py3 as falc-py3
COPY fal-library/firmware_schema.xsd /src/falc-program/fpm-template/usr/share/fall/firmware_schema.xsd
COPY fal-library/firmware_info.db /src/falc-program/fpm-template/usr/share/fall/firmware_info.db
RUN source /venv-py3/bin/activate && \
    mkdir -p /output && \
    set -o pipefail && \
    packaging/build-exe-py3.sh falc deb && cp -v dist/*.deb /output

# output container
FROM base as output
COPY --from=falc-py3 /output /output
COPY falc-program/installer/install-fal.sh /output
COPY falc-program/installer/uninstall-fal.sh /output

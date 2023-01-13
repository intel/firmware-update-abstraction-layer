# base image with all dependencies for building
FROM registry.hub.docker.com/library/ubuntu:20.04 as base
include(`commands.base-setup.m4')

FROM base as packaging
COPY packaging /src/packaging
COPY firmware_info.db /src/packaging
COPY firmware_schema.xsd /src/packaging
WORKDIR /src/packaging
RUN rm -rf output/ && \
    mkdir -p output/ && \
    ./configure && \
    make clean
RUN make build && \
    mkdir -p /output/coverage && \
    mv output/* /output
WORKDIR /repo
WORKDIR /src/packaging


# build a virtual environment for each agent to build from

# py3 venv
FROM base as venv-py3
WORKDIR /
RUN python3.10 -m venv /venv-py3 && \
    source /venv-py3/bin/activate && \
    pip3.10 install --upgrade pip && \
    pip3.10 install teamcity-messages==1.31 virtualenv==20.16.3 wheel==0.37.1 -U
RUN source /venv-py3/bin/activate

# ---fall---

FROM venv-py3 as venv-fall-py3
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN source /venv-py3/bin/activate && \
    pip3.10 install -r requirements.txt
COPY version.txt /src/version.txt
COPY setup.py /src/setup.py
COPY fall /src/fall

FROM venv-fall-py3 as fall
COPY python-config/pyproject.toml /src
WORKDIR /src
ARG VERSION
ARG COMMIT
RUN mkdir -p /src/fpm-template/usr/share/fall/ && \
    ( echo "Version: ${VERSION}" && echo "Commit: ${COMMIT}" ) >/src/fpm-template/usr/share/fall/fall-version.txt
RUN source /venv-py3/bin/activate && \
    mkdir -p /output && \
    set -o pipefail && python setup.py sdist bdist_wheel && cp -v dist/*.whl /output

# output container
FROM base as output
COPY --from=packaging /output /packaging
COPY --from=fall /output /fall
RUN mkdir -p /output && \
    cp -rv /fall/* \
    /packaging/* \
    /output

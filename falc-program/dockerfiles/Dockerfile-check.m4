# base image with all dependencies for running unit tests/lints
FROM registry.hub.docker.com/library/ubuntu:20.04 as base

SHELL ["/bin/bash", "-c"]
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get clean
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3.10-venv \
    python3-setuptools \
    build-essential \
    && \
    apt-get clean


# build a virtual environment to run checks

# py3 venv
FROM base as venv-py3
WORKDIR /
RUN python3.10 -m venv /venv-py3 && \
    source /venv-py3/bin/activate && \
    pip3.10 install --upgrade pip && \
    pip3.10 install wheel==0.34.2 && \
    pip3.10 install \
        pytest==7.1.2 \
        pytest-cov==3.0.0 \
        flake8==4.0.1 \
        bandit==1.7.4 \
        flake8-bandit==3.0.0 \
        coverage==6.4.4 \
        flakeheaven==3.0.0 \
        wemake-python-styleguide==0.16.1 \
        teamcity-messages==1.31 \
        mock==4.0.3 \
        types-mock==4.0.15 \
        pylint==2.14.5 \
        mypy==0.971 \
        -U

# ---falc-program---

FROM venv-py3 as venv-falc-py3
COPY falc-program/requirements.txt /src/falc-program/requirements.txt
COPY falc-program/packaging /src/packaging
RUN cp /src/packaging/*.whl /src/falc-program
COPY falc-program/test-requirements.txt /src/falc-program/test-requirements.txt
WORKDIR /src/falc-program
RUN source /venv-py3/bin/activate && \
    pip3 install -r requirements.txt && \
    pip3 install -r test-requirements.txt
COPY falc-program /src/falc-program

RUN apt install tree && tree
COPY falc-program/python-config /python-config
RUN source /venv-py3/bin/activate && \
    cp -f /python-config/pyproject.toml . && \
    flakeheaven lint

FROM venv-falc-py3 as mypy-falc
RUN source /venv-py3/bin/activate && \
    /python-config/mypy-py3.sh falc && \
    touch /passed.txt

FROM venv-falc-py3 as falc-unit-tests
RUN source /venv-py3/bin/activate && \
    mkdir -p /output/coverage && \
    set -o pipefail && \
    cd falc && \
    pytest --cov=falc tests/unit 2>&1 | tee /output/coverage/falc-coverage.txt && \
    coverage report --show-missing --fail-under=93

# output container
FROM base as output
COPY --from=falc-unit-tests /output /falc
COPY --from=mypy-falc /passed.txt /passed-mypy-falc.txt
#COPY --from=lint-venv-py3 /passed.txt /passed-lint-venv-py3.txt
RUN mkdir -p /output/ && \
    cp -rv \
    /falc/* \
    /output

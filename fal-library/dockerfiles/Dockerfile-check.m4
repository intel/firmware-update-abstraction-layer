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
COPY /python-config /python-config
RUN python3.10 -m venv /venv-py3 && \
    source /venv-py3/bin/activate && \
    pip3.10 install --upgrade pip && \
    pip3.10 install wheel==0.34.2 && \
    pip3.10 install \
        pytest==7.1.2 \
        atheris==2.0.12 \
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
ENV PYTHONPATH=/src/fal-library/fall

# ---fal-library---

FROM venv-py3 as venv-fall-py3
COPY requirements.txt /src/fal-library/fall/requirements.txt
COPY test-requirements.txt /src/fal-library/fall/test-requirements.txt
WORKDIR /src/fal-library/fall
RUN source /venv-py3/bin/activate && \
    pip3.10 install -r requirements.txt && \
    pip3.10 install -r test-requirements.txt
COPY fall /src/fal-library/fall
COPY packaging /src/fal-library/packaging
RUN source /venv-py3/bin/activate && \
    cp -f /python-config/pyproject.toml . && \
    flakeheaven lint

FROM venv-fall-py3 as mypy-fall
RUN source /venv-py3/bin/activate && \
    /python-config/mypy-py3.sh . && \
    touch /passed.txt

FROM venv-fall-py3 as fall-unit-tests
COPY firmware_info.db /src/fal-library/fall/db/firmware_info.db
COPY firmware_schema.xsd /src/fal-library/fall/schema/firmware_schema.xsd

RUN source /venv-py3/bin/activate && \
    mkdir -p /output/coverage && \
    set -o pipefail && \
    cd /src/fal-library/fall && \
    pytest --ignore=tests/fuzz --cov=fall tests/unit 2>&1 | tee /output/coverage/fall-coverage.txt && \
    coverage report --show-missing --fail-under=93

FROM venv-fall-py3 as fall-fuzz-tests
RUN source /venv-py3/bin/activate && \
    cd /src/fal-library && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_query.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_autofill.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_guid.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_manufacturer.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_path.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_platform_name.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_release_date.py -atheris_runs=10000 --debug=trace && \
    python3 -m coverage run ./fall/tests/fuzz/test_fuzz_fw_vendor.py -atheris_runs=10000 --debug=trace

# output container
FROM base as output
COPY --from=fall-unit-tests /output /fall
COPY --from=mypy-fall /passed.txt /passed-mypy-fall.txt
RUN mkdir -p /output/ && \
    cp -rv \
    /fall/* \
    /output

# base-setup.m4: common set of commands for a base utility image, either x86 or arm

SHELL ["/bin/bash", "-c"]
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get clean
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -y \
    m4 \
    build-essential \
    curl \
    ruby-dev \
    rubygems \
    pkg-config \
    wget \
    unzip \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3.10-venv \
    python3-setuptools \
    libxslt1-dev \
    gcc \
    cpio \
    git && \
    apt-get clean
RUN gem install --no-document fpm

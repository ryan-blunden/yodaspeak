FROM ubuntu:noble
LABEL maintainer="Ryan Blunden <ryan.blunden@gmail.com>"

# Change to bust the Docker cache and install latest package versions
ARG LAST_UPDATED=2025-01-22

ENV DEBIAN_FRONTEND="noninteractive"
ENV DOPPLER_ENV="1"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PIP_NO_CACHE_DIR="off"
ENV PIP_DISABLE_PIP_VERSION_CHECK="1"
ENV PYTHONPATH="."
ENV PATH="${PATH}:/home/coder/.local/bin"
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN \
  # Add Docker's official GPG key and add repository to apt sources
  apt-get update && \
  apt-get upgrade --yes --no-install-recommends --no-install-suggests && \
  apt-get install --yes --no-install-recommends --no-install-suggests ca-certificates curl && \
  install -m 0755 -d /etc/apt/keyrings && \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
  chmod a+r /etc/apt/keyrings/docker.asc && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null && \
  apt-get update && \
  \
  apt-get install -y --no-install-recommends --no-install-suggests \
    # System dependencies
    build-essential \
    software-properties-common \
    \
    # Docker components
    docker-ce \
    docker-ce-cli \
    containerd.io \ 
    docker-buildx-plugin \
    docker-compose-plugin \
    \
    # systemd for running Docker service
    systemd \
    systemd-sysv \
    \
    # Utilities
    git \
    bash-completion \
    nano \
    locales \
    jq \
    sudo \
    \
    # Python app dependencies for local development
    pipx \
    python3 \
    python3-pip \
    postgresql-client && \
    \
    # Install Doppler CLI for secrets injection
    wget -t 3 -qO- https://cli.doppler.com/install.sh | sh && \
    \ 
    # Cleanup
    rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man && \
    apt-get clean

# Enable Docker service with systemd
RUN systemctl enable docker

# Create a symlink for standalone docker-compose usage
RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose

# Generate the default locale
RUN locale-gen en_US.UTF-8

# Add `coder` user to avoid developing as root
RUN userdel -r ubuntu && \
    useradd coder \
    --create-home \
    --shell=/bin/bash \
    --groups=docker \
    --uid=1000 \
    --user-group && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >>/etc/sudoers.d/nopasswd

USER coder
WORKDIR /home/coder
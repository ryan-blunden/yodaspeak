FROM python:3.13
LABEL maintainer="Ryan Blunden <ryan.blunden@gmail.com>"

ENV DEBIAN_FRONTEND="noninteractive"
ENV DOPPLER_ENV="1"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PIP_NO_CACHE_DIR="off"
ENV PIP_DISABLE_PIP_VERSION_CHECK="1"
ENV PYTHONPATH="."
ENV PATH="${PATH}:/home/yodaspeak/.local/bin"

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  vim \
  locales-all \
  jq \
  sudo && \
  rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man && \
  apt-get clean && \
  \
  (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh

# Add a user `coder` so that you're not developing as `root`
RUN useradd coder \
    --groups sudo \
    --no-create-home \
    --shell /bin/bash && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/coder && \
    chmod 0440 /etc/sudoers.d/coder

USER coder
WORKDIR /home/coder

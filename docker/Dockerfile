FROM python:3.13
LABEL maintainer="Ryan Blunden <ryan.blunden@gmail.com>"

ARG UID=1000
ARG GID=1000

ENV DOPPLER_ENV="1"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PIP_DISABLE_PIP_VERSION_CHECK="1"
ENV PYTHONPATH="."
ENV PATH="${PATH}:/home/yodaspeak/.local/bin"

# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#   build-essential \
#   pipx \
#   vim \
#   htop \
#   jq \
#   locales \
#   && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
#   && apt-get clean && \
#   \
#   (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sudo sh

RUN (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sudo sh

WORKDIR /app

RUN groupadd -g "${GID}" yodaspeak \
&& useradd --create-home --no-log-init -u "${UID}" -g "${GID}" yodaspeak\
  && chown yodaspeak:yodaspeak -R /app

USER yodaspeak

COPY --chown=yodaspeak:yodaspeak requirements/ ./requirements
COPY --chown=yodaspeak:yodaspeak bin/ ./bin

RUN chmod 0755 bin/* && \
pip install --no-warn-script-location --no-cache-dir --user -r requirements/production.txt

COPY --chown=yodaspeak:yodaspeak . .

WORKDIR /app/src

ENTRYPOINT ["/app/bin/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "-c", "python:config.gunicorn", "config.wsgi"]

FROM python:3.13.0-slim-bookworm
LABEL maintainer="Ryan Blunden <ryan.blunden@gmail.com>"

ENV DOPPLER_ENV=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONPATH="."
ENV PATH="${PATH}:/home/yodaspeak/.local/bin"

WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" yodaspeak \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" yodaspeak \
  && chown yodaspeak:yodaspeak -R /usr/src/app

USER yodaspeak

COPY --chown=yodaspeak:yodaspeak requirements ./
COPY --chown=yodaspeak:yodaspeak bin/ ./bin

RUN chmod 0755 bin/* && \
pip install --no-warn-script-location --no-cache-dir --user -r requireents/production.txt

COPY --chown=yodaspeak:yodaspeak . .

ENTRYPOINT ["/usr/src/app/bin/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "-c", "yodaspeak:config.gunicorn", "config.wsgi"]

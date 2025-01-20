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

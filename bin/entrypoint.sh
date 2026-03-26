#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

if [ "${DJANGO_COLLECTSTATIC,,}" == "true" ]; then
  echo "[info] Collecting static files."
  ./manage.py collectstatic --noinput
fi

if [ "${DJANGO_MIGRATE,,}" == "true" ]; then
  echo "[info] Running migrations."
  ./manage.py migrate --noinput
fi

if [ "${DEBUG,,}" != "true" ]; then
  ./manage.py check --deploy
fi

echo "[info] Starting: $*"
exec "$@"

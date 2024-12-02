#!/usr/bin/env bash

set -e

set -o errexit
set -o pipefail
set -o nounset

#--------------------------------------------
# ENTRYPOINT SCRIPT
#
#  - Database is assumed to be created.
#  - Django admin user is not created as part of this.
#
#--------------------------------------------

#-------------------------------------------------------------------------------
# Optional operations before application start
#-------------------------------------------------------------------------------

if [ -v INSTALL_DEV_PACKAGES ] && [ ! -f /tmp/.dev-packages-installed ]; then
    echo '[info]: Installing development packages as INSTALL_DEV_PACKAGES is set.'
    pip install -r /app/requirements/local.txt
    touch /tmp/.dev-packages-installed
fi

if [ -v DJANGO_COLLECTSTATIC ]; then
    echo '[info]: Collecting static resources as DJANGO_COLLECTSTATIC is set.'
    ./manage.py collectstatic --noinput
fi

if [ -v DJANGO_MIGRATE ]; then
    echo '[info]: Performing database migrations as DJANGO_MIGRATE is set.'
    ./manage.py migrate --noinput
fi

if [ -z DEBUG ]; then
    ./manage.py check --deploy
fi


#-------------
# Start!
#-------------

# Generate SENTRY_RELEASE environment variable for release tracking
# TODO

echo "[info]: Starting application with command - \"${@}.\""
exec "$@"


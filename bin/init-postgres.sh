#! /usr/bin/env bash

set -e

echo -e "\n[info]: initializing database $POSTGRES_DB with $POSTGRES_USER user."

cat << EOF  > init-db.sql
CREATE DATABASE "$POSTGRES_DB";
CREATE USER "$POSTGRES_USER" WITH PASSWORD '$POSTGRES_PASSWORD';
ALTER ROLE "$POSTGRES_USER" SET client_encoding TO 'utf8';
ALTER ROLE "$POSTGRES_USER" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "$POSTGRES_USER" SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOF

PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql --username="$POSTGRES_ADMIN_USER" --host="$POSTGRES_HOST" < init-db.sql
rm init-db.sql

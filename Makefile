.PHONY: help install dev-server test docker docker-compose docker-compose-data
.DEFAULT_GOAL := help
SHELL := /bin/bash

help:
	@printf '%s\n' \
	  'Available targets:' \
	  '  install' \
	  '  dev-server' \
	  '  test' \
	  '  docker' \
	  '  docker-compose' \
	  '  docker-compose-data'

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements/local.txt
	.venv/bin/python manage.py migrate

dev-server:
	.venv/bin/python manage.py runserver 0.0.0.0:8000

test:
	.venv/bin/python manage.py test

docker:
	docker run \
	  -it \
	  --rm \
	  --name yodaspeak \
	  --env-file .env \
	  -p 8000:8000 \
	  ghcr.io/ryan-blunden/yodaspeak:latest

docker-compose:
	docker-compose up --build

docker-compose-data:
	docker compose --profile data up --build

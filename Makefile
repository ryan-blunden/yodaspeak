SHELL := /bin/bash

lint:
	flake8 ./src

sort_imports:
	isort ./src

format:
	black ./

lint-dockerfile:
	docker run --rm -i hadolint/hadolint hadolint - < "coder/Dockerfile"

docker-app-build:
	docker image pull python:3.13
	docker buildx build -t ryanblunden/yodaspeak:$(version) . --platform linux/arm/v7,linux/arm64/v8,linux/amd64

docker-app-push:
	docker image push ryanblunden/yodaspeak:$(version)

dev-server:
	./src/manage.py runserver_plus 0.0.0.0:8000

doppler-run-dev-server:
	doppler run -- ./src/manage.py runserver_plus 0.0.0.0:8000

doppler-docker-compose-up:
	trap 'rm -f .env; exit' INT TERM; \
	doppler secrets download --no-file --format docker > .env && \
	docker compose up; \
	rm -f .env

doppler-docker-compose-reset:
	trap 'rm -f .env; exit' INT TERM; \
	doppler secrets download --no-file --format docker > .env && \
	docker compose down -v; \
	rm -f .env

#___ CODER ___#

docker-coder-build:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f coder/Dockerfile --platform linux/arm/v7,linux/arm64/v8,linux/amd64

docker-coder-push:
	docker image push ryanblunden/yodaspeak-coder:$(version)

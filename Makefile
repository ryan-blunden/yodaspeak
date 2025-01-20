SHELL := /bin/bash

lint:
	flake8 ./src

sort_imports:
	isort ./src

format:
	black ./

lint-dockerfile:
	docker run --rm -i hadolint/hadolint hadolint - < "coder/Dockerfile"

docker-app-build-amd64:
	docker buildx build -t ryanblunden/yodaspeak:$(version) . --platform linux/amd64

docker-app-build-arm64:	
	docker buildx build -t ryanblunden/yodaspeak:$(version) . --platform linux/arm64

docker-app-push-amd64:
	docker image push ryanblunden/yodaspeak:$(version) --platform linux/amd64

docker-app-push-arm64:
	docker image push ryanblunden/yodaspeak:$(version) --platform linux/arm64

dev-server:
	./src/manage.py runserver_plus 0.0.0.0:8000

doppler-run-dev-server:
	doppler run -- ./src/manage.py runserver_plus 0.0.0.0:8000

doppler-run-docker-compose:
	doppler run --mount .env --mount-format docker -- docker compose up


#___ CODER ___#

docker-coder-build-amd64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f coder/Dockerfile --platform linux/amd64

docker-coder-build-arm64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f coder/Dockerfile --platform linux/arm64

docker-coder-push-amd64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/amd64

docker-coder-push-arm64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/arm64
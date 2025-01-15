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
	docker buildx build -t ryanblunden/yodaspeak:$(version) . -f docker/Dockerfile --platform linux/amd64

docker-app-build-arm64:	
	docker buildx build -t ryanblunden/yodaspeak:$(version) . -f docker/Dockerfile --platform linux/arm64

docker-app-push-amd64:
	docker image push ryanblunden/yodaspeak:$(version) --platform linux/amd64

docker-app-push-arm64:
	docker image push ryanblunden/yodaspeak:$(version) --platform linux/arm64

docker-coder-build-amd64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f coder/Dockerfile --platform linux/amd64

docker-coder-build-arm64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f coder/Dockerfile --platform linux/arm64

docker-coder-push-amd64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/amd64

docker-coder-push-arm64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/arm64

docker-app-run:
	docker run \
	--rm \
	-it -p 8000:8000 \
	--env-file <(doppler secrets download --no-file --format docker) \
	-v $$PWD:/app \
	--entrypoint /bin/bash \
	--workdir /app \
	ryanblunden/yodaspeak

app-venv-setup:
	cd src && \
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r ../requirements/local.txt

dev-server:
	./src/manage.py runserver_plus 0.0.0.0:8000

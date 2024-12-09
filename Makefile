lint:
	flake8 ./src

sort_imports:
	isort ./src

format:
	black ./

lint-dockerfile:
	docker run --rm -i hadolint/hadolint hadolint - < "Docker/Coder.Dockerfile"

docker-build:
	docker buildx build -t ryanblunden/yodaspeak:$(version) . -f docker/Dockerfile --platform linux/amd64
	docker buildx build -t ryanblunden/yodaspeak:$(version) . -f docker/Dockerfile --platform linux/arm64

docker-coder-build-amd64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f docker/Coder.Dockerfile --platform linux/amd64

docker-coder-build-arm64:
	docker buildx build -t ryanblunden/yodaspeak-coder:$(version) . -f docker/Coder.Dockerfile --platform linux/arm64

docker-coder-push-amd64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/amd64

docker-coder-push-arm64:
	docker image push ryanblunden/yodaspeak-coder:$(version) --platform linux/arm64

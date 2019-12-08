.PHONY: *

all: clean deps-sync deps-check lint test build

deps-sync:
	pipenv sync --dev --bare

deps-check:
	pipenv check

deps-update:
	pipenv --rm
	pipenv update --dev

lint:
	pipenv run flake8
	pipenv run black --check --diff --verbose .

test:
	pipenv run pytest -v --color=yes --cov=asgard

build: build-binary

build-binary:
	pipenv run pyinstaller asgard.spec

build-docker:
	docker build . -t claudeleveille/asgard:latest

clean:
	git clean -dfx -e .vscode/ -e .idea/

fmt:
	pipenv run black --verbose .

release: clean build-binary
	if [ "$$(git branch --show-current |tr -d '\n')" = "master" ]; then \
		echo "__version__ = \"$$(./dist/asgard)\"" > asgard/_version.py; \
		git add asgard/_version.py; \
		./dist/asgard --commit --tag; \
		git push origin master; \
		git push --tags origin; \
	else \
		echo "Not releasing because current branch isn't master"; \
	fi

all: setup format test build

setup: deps.install deps.install/dev branch/init

deps.install:
	pip install -e .
deps.install.reqs:
	pip install -r requirements.txt
deps.install/dev:
	pip install -e ".[dev]"
deps.install.reqs/dev:
	pip install -r requirements.dev.txt
deps.freeze:
	python -m pip freeze --local --exclude-editable > requirements.txt
deps.freeze/dev:
	python -m pip freeze --local --exclude-editable > requirements.dev.txt
deps/reqs:
	pipreqs . --savepath requirements.prod.txt
deps/outdated:
	python -m pip list --outdated
deps/check:
	python -m pip check

branch/init:
	python -m branch init

.PHONY: run
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
run:
	python -m branch $(RUN_ARGS)
run/server:
	python -m branch server start --storage-location='local://.branch'

format:
	python -m ruff format .
format/check:
	python -m ruff format --check .

typecheck:
	python -m pyright

lint:
	python -m ruff check .

test:
	pytest -vv --no-header --record-mode=once src
test/watch:
	ptw -vv --no-header --record-mode=once src
test/nocapture:
	pytest -vv --no-header --capture=no --record-mode=once src

coverage:
	pytest --cov src

.PHONY: build
build: build/pyinstaller
build/pyinstaller:
	pyinstaller \
		--additional-hooks-dir=./src/branch/pyinstaller/hooks \
		--onefile \
		--name branch \
		src/branch/main.py
build/nuitka:
	python -m nuitka \
		--standalone \
		--onefile \
		--prefer-source-code \
		--output-dir=nuitka \
		--output-filename=branch \
		src/branch/main.py

.PHONY: exec exec/pyinstaller exec/nuitka
ifeq (exec,$(firstword $(MAKECMDGOALS)))
  EXEC_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(EXEC_ARGS):;@:)
endif
exec: exec/pyinstaller
ifeq (exec/pyinstaller,$(firstword $(MAKECMDGOALS)))
  EXEC_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(EXEC_ARGS):;@:)
endif
exec/pyinstaller:
	./dist/branch $(EXEC_ARGS)
ifeq (exec/nuitka,$(firstword $(MAKECMDGOALS)))
  EXEC_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(EXEC_ARGS):;@:)
endif
exec/nuitka:
	./nuitka/branch $(EXEC_ARGS)

package.zip/linux-x86_64:
	zip -r dist/branch-linux-x86_64.zip dist/branch
package.zip/darwin-aarch64:
	zip -r dist/branch-darwin-aarch64.zip dist/branch
package.zip/win-x86_64:
	zip -r dist/branch-win-x86_64.zip dist/branch.exe

clean: clean/deps clean/build
clean/deps:
	rm -rf .venv
clean/build:
	rm -rf build
	rm -rf dist
	rm -rf nuitka
	rm -rf *.spec

compose.build:
	docker compose build
compose.up:
	docker compose up
docker.build/deps:
	DOCKER_BUILDKIT=1 \
									docker build \
									-f docker/Dockerfile \
									--cache-from "mechanical-orchard/branch:deps" \
									--target deps \
									--build-arg BUILDKIT_INLINE_CACHE=1 \
									-t mechanical-orchard/branch:deps \
									.
docker.build/run:
	DOCKER_BUILDKIT=1 \
									docker build \
									-f docker/Dockerfile \
									--cache-from "mechanical-orchard/branch:deps" \
									--cache-from "mechanical-orchard/branch:latest" \
									--target run \
									--build-arg BUILDKIT_INLINE_CACHE=1 \
									-t mechanical-orchard/branch:latest \
									.

ollama/start:
	ollama start

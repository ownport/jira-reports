PYTHON ?= /usr/bin/env python
PROJECT_NAME_BIN ?= jirareports
PROJECT_NAME_SRC ?= jirareports

clean:
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/.local-ci
	@ rm -rf $(shell pwd)/.local-ci
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/jirareports.egg-info
	@ rm -rf $(shell pwd)/jirareports.egg-info
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/bin
	@ rm -rf $(shell pwd)/bin
	@ echo "[INFO] Cleaning files: *.pyc"
	@ find . -name "*.pyc" -delete
	@ echo "[INFO] Cleaning files: .coverage"
	@ rm -rf $(shell pwd)/.coverage


compile: clean
	@ echo "[INFO] Compiling to binary, $(PROJECT_NAME_BIN)"
	@ mkdir -p $(shell pwd)/bin
	@ cd $(shell pwd)/$(PROJECT_NAME_SRC)/; zip --quiet -r ../bin/$(PROJECT_NAME_BIN) *
	@ echo '#!$(PYTHON)' > bin/$(PROJECT_NAME_BIN) && \
		cat bin/$(PROJECT_NAME_BIN).zip >> bin/$(PROJECT_NAME_BIN) && \
		rm bin/$(PROJECT_NAME_BIN).zip && \
		chmod a+x bin/$(PROJECT_NAME_BIN)

sdist:
	@ python setup.py sdist


build-dev-docker-images:
	@ docker build --tag ownport/jirareports-dev-env:py2.7 .


test-all: clean
	@ py.test


test-all-with-coverage: clean
	@ py.test --cov=jirareports --cov-report term-missing --cov-config=.coveragerc


run-local-ci: clean
	@ local-ci -r $(shell pwd) -s .local-ci.yml

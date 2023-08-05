PIPENV ?= $(shell which pipenv)

devdeps: .devdeps

.devdeps: Pipfile.lock
	$(PIPENV) install --dev --ignore-pipfile
	touch .devdeps

lint: devdeps
	$(PIPENV) run flake8

build: devdeps lint
	$(PIPENV) run flit build

deploy: devdeps
	$(PIPENV) run flit publish

define ALL
	update-requirements
endef
ALL:=$(shell echo $(ALL))  # to remove line-feeds

define REQUIREMENTS_FILES
	requirements/dev.txt
	requirements/docs.txt
	requirements/lint.txt
	requirements/test.txt
	requirements/site.txt
	requirements.txt
endef
REQUIREMENTS_FILES:=$(shell echo $(REQUIREMENTS_FILES))

define REQUIREMENTS_IN
	requirements.in
endef
REQUIREMENTS_IN:=$(shell echo $(REQUIREMENTS_IN))

define REQUIREMENTS_IN_SITE
	requirements.in
	requirements/site.in
endef
REQUIREMENTS_IN_SITE:=$(shell echo $(REQUIREMENTS_IN_SITE))

define REQUIREMENTS_IN_TEST
	requirements/test.in
	requirements.in
endef
REQUIREMENTS_IN_TEST:=$(shell echo $(REQUIREMENTS_IN_TEST))

define REQUIREMENTS_IN_LINT
	requirements/lint.in
endef
REQUIREMENTS_IN_LINT:=$(shell echo $(REQUIREMENTS_IN_LINT))

define REQUIREMENTS_IN_DOCS
	requirements/docs.in
	requirements.in
endef
REQUIREMENTS_IN_DOCS:=$(shell echo $(REQUIREMENTS_IN_DOCS))

define REQUIREMENTS_IN_DEV
	requirements/dev.in
	requirements/docs.in
	requirements/lint.in
	requirements/test.in
	requirements/site.in
	requirements.in
endef
REQUIREMENTS_IN_DEV:=$(shell echo $(REQUIREMENTS_IN_DEV))


VENV	:= . bin/activate &&


.PHONY: all
all: $(REQUIREMENTS_FILES) update-requirements

.PHONY: update-requirements
update-requirements: .pip-sync
.pip-sync: requirements/dev.txt
	$(VENV) pip-sync $^
	$(VENV) pip freeze > $@.tmp && mv $@.tmp $@

requirements.txt: $(REQUIREMENTS_IN)
	$(VENV)	pip-compile $(pip-compile-options) -o $@ $^
	$(VENV)	pip wheel --no-deps -r $@ -w virtualenv_support

requirements/site.txt: $(REQUIREMENTS_IN_SITE)
	$(VENV) pip-compile $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel --no-deps -r $@

requirements/test.txt: $(REQUIREMENTS_IN_TEST)
	$(VENV) pip-compile $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel --no-deps -r $@

requirements/lint.txt: $(REQUIREMENTS_IN_LINT)
	$(VENV) pip-compile $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel --no-deps -r $@

requirements/docs.txt: $(REQUIREMENTS_IN_DOCS)
	$(VENV) pip-compile $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel --no-deps -r $@

requirements/dev.txt: $(REQUIREMENTS_IN_DEV)
	$(VENV) pip-compile $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel --no-deps -r $@

.PHONY: test
test: requirements/test.txt
	$(VENV) tox -e py27,py34,pypy
	$(VENV) coverage combine
	$(VENV) coverage report

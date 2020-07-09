CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest

IP	 ?= 127.0.0.1
PORT ?= 19999

WGET = wget -c --no-check-certificate



.PHONY: all py test web
all: py

py: $(PY) $(MODULE).py $(MODULE).ini
	$(MAKE) test
	IP=$(IP) PORT=$(PORT) $(PY) -i $(MODULE).py
test: $(PYT) test_$(MODULE).py
	IP=$(IP) PORT=$(PORT) $^
# 	py.test --cov=metaL test_metaL.py
# 	coverage html
web: $(PY) web.py $(MODULE).py $(MODULE).ini
	IP=$(IP) PORT=$(PORT) $^



.PHONY: install update

install: $(OS)_install $(PIP) js
	$(PIP) install    -r requirements.txt
	$(MAKE) requirements.txt

update: $(OS)_update $(PIP)
	$(PIP) install -U    pip
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
	$(MAKE) requirements.txt
$(PYT):
	$(PIP) install -U pytest
	$(MAKE) requirements.txt

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@

.PHONY: Linux_install Linux_update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`


.PHONY: js
js: static/jquery.js static/bootstrap.css static/bootstrap.js

JQUERY_VER = 3.5.0
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js

BOOTSTRAP_VER = 3.4.1
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js



.PHONY: master shadow release

MERGE  = Makefile README.md .gitignore .vscode apt.txt requirements.txt
MERGE += $(MODULE).py test_$(MODULE).py $(MODULE).ini web.py static templates config.py

master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@
	git pull -v

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow

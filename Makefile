CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest

HOST ?= 127.0.0.1
PORT ?= 19999

WGET = wget -c --no-check-certificate



%: $(PY) $(MODULE).py %.py $(PYT) test_$(MODULE).py test_%.py
	$(PYT) test_$(MODULE).py test_$@.py
	$(PY) -i $@.py

TESTS = $(shell ls test_*.py)
.PHONY: test
test: $(PYT) $(TESTS)
	HOST=$(HOST) PORT=$(PORT) $^
# 	py.test --cov=metaL test_metaL.py
# 	coverage html



.PHONY: install update

install: $(OS)_install $(PIP) js doc libtcc
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



doc: doc/SICP_ru.pdf doc/SICP_en.pdf
doc/SICP_ru.pdf:
	$(WGET) -O $@ http://newstar.rinet.ru/~goga/sicp/sicp.pdf
doc/SICP_en.pdf:
	$(WGET) -O $@ https://web.mit.edu/alexmv/6.037/sicp.pdf



.PHONY: master shadow release

MERGE  = Makefile README.md .gitignore apt.txt requirements.txt
MERGE += $(MODULE).py test_$(MODULE).py $(MODULE).ini web.py static templates config.py
MERGE += metacirc.py emlinux.py nim.py rwd.py nimde.py redisview.py
MERGE += $(MODULE) emlinux
MERGE += doc
MERGE += test_parser.py parser.py

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



TCC_VER = 0.9.27
TCC     = tcc-$(TCC_VER)
TCC_GZ  = $(TCC).tar.bz2

TMP = $(CWD)/tmp

gz: $(TMP)/$(TCC_GZ)
$(TMP)/$(TCC_GZ):
	$(WGET) -O $@ http://download.savannah.gnu.org/releases/tinycc/$(TCC_GZ)

.PHONY: libtcc
libtcc: tcclib/lib/libtcc.so
tcclib/lib/libtcc.so:
	$(MAKE) $(TMP)/$(TCC)/README
	cd $(TMP)/$(TCC) ;\
	./configure --prefix=$(CWD)/tcclib --cc=tcc --disable-static &&\
	$(MAKE) -j4 && $(MAKE) install
	rm -rf $(TMP)/$(TCC) $(TMP)/$(TCC_GZ)
$(TMP)/$(TCC)/README: $(TMP)/$(TCC_GZ)
	cd $(TMP) ; bzcat $< | tar x && touch $@

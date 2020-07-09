CWD     = $(CURDIR)
MODULE  = $(shell echo $(notdir $(CWD)) | tr "[:upper:]" "[:lower:]" )
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

.PHONY: all
all: book test jslibs

book:
	$(MAKE) -C book
	
pdf: $(MODULE)_$(TODAY).pdf
$(MODULE)_$(TODAY).pdf: book/$(MODULE).pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
		-dNOPAUSE -dQUIET -dBATCH \
		-sOutputFile=$@ $<
# /screen /ebook /prepress
#	$(MAKE) all && $(MAKE) pdf

merge:
	$(MAKE) pdf
	git checkout master
	git checkout ponyatov -- Makefile book/ metaL.py metaL.ml
	
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags

test:
	py.test --cov=metaL test_metaL.py
	coverage html

jslibs: static/go.js

static/go.js:
	wget -c -O $@ https://cdnjs.cloudflare.com/ajax/libs/gojs/2.0.5/go.js

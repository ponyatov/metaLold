MODULE = $(notdir $(CURDIR))
TODAY = $(shell date +%d%m%y)

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
	git tag $(TODAY) && git push --tags

test:
	py.test --cov=metaL test_metaL.py
	coverage html

jslibs: static/go.js

static/go.js:
	wget -c -O $@ https://cdnjs.cloudflare.com/ajax/libs/gojs/2.0.5/go.js

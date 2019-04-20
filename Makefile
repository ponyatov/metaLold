MODULE = $(notdir $(CURDIR))
TODAY = $(shell date +%d%m%y)

all:
	$(MAKE) -C book
	$(MAKE) -C Android
	$(MAKE) -C game
	
pdf: $(MODULE)_$(TODAY).pdf
$(MODULE)_$(TODAY).pdf: book/$(MODULE).pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
		-dNOPAUSE -dQUIET -dBATCH \
		-sOutputFile=$@ $<
# /screen /ebook /prepress

release:
	$(MAKE) all && $(MAKE) pdf
	git tag $(TODAY) && git push --tags

update:
#	git submodule update --init --recursive
	git pull -v
	cd Ouroboros ; git pull -v
	cd mcu ; git pull -v
	cd mcu/LoRaMac-node ; git pull -v

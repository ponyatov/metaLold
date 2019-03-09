
TODAY = $(shell date +%d%m%y)

all:
	$(MAKE) -C book
	
pdf: hico_$(TODAY).pdf
hico_$(TODAY).pdf: book/hico.pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
		-dNOPAUSE -dQUIET -dBATCH \
		-sOutputFile=$@ $<
# /screen /ebook /prepress

release:
	$(MAKE) all && $(MAKE) pdf
	git tag $(TODAY) && git push --tags

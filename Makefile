
TODAY = $(shell date +%d%m%y)

all:
	$(MAKE) -C book
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
		-dNOPAUSE -dQUIET -dBATCH \
		-sOutputFile=hico_$(TODAY).pdf book/hico.pdf
	echo make release

release:
	$(MAKE) all
	git tag $(TODAY) && git push --tags
	
# /screen /ebook /prepress

# https://www.kv.by/archive/index2010503001.htm

SRC  = META-INF/container.xml
SRC += content.html
SRC += content.opf
SRC += cover.html
SRC += ouroboros.png
SRC += style.css
SRC += toc.ncx

TODAY = $(shell date +%d%m%y)

all: ../hico_$(TODAY).epub

../hico_$(TODAY).epub: mimetype $(SRC) Makefile
	rm -f $@
	zip -0X $@ $<
	zip -Xr9D $@ $(SRC)
	java -jar epubcheck.jar $@

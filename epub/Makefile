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
	zip -0X $@ $<
	zip -Xr9D $@ $(SRC)

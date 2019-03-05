
all:
	echo make release

TODAY = $(shell date +%d%m%y)
release:
	$(MAKE) -C book
	cp book/hico.pdf hico_$(TODAY).pdf
	git tag $(TODAY) && git push --tags

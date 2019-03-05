TEX  = hico.tex header.tex
TEX += intro/intro.tex intro/meta.tex intro/homoiconic.tex
TEX += frames/frames.tex
TEX += bib/bib.tex

LATEX = pdflatex -halt-on-error

book.pdf: $(TEX)
	$(LATEX) $< && $(LATEX) $<

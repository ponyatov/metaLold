TEX = hico.tex header.tex
TEX += bib/bib.tex

LATEX = pdflatex -halt-on-error

book.pdf: $(TEX)
	$(LATEX) $< && $(LATEX) $<

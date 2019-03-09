TEX  = hico.tex header.tex
TEX += intro/intro.tex intro/denial.tex intro/meta.tex 
TEX += intro/brooks.tex intro/lop.tex intro/homoiconic.tex
TEX += frames/frames.tex
TEX += forth/forth.tex
TEX += web/web.tex
TEX += dyna/dyna.tex dyna/llvm.tex
TEX += prolog/prolog.tex
TEX += bib/bib.tex

LST  = lst/frame.py

LATEX = pdflatex -halt-on-error

book.pdf: $(TEX) $(LST) $(FIG)
	$(LATEX) $< && $(LATEX) $<

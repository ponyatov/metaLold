TEX  = hico.tex header.tex

TEX += intro/intro.tex intro/denial.tex intro/meta.tex 
TEX += intro/brooks.tex intro/lop.tex intro/homoiconic.tex

TEX += frames/frames.tex frames/frame.tex frames/dump.tex
TEX += frames/prim.tex frames/string.tex frames/symbol.tex frames/number.tex
TEX += frames/container.tex frames/stack.tex frames/dict.tex

TEX += forth/forth.tex forth/dict.tex forth/ply.tex
TEX += web/web.tex
TEX += dyna/dyna.tex dyna/llvm.tex
TEX += prolog/prolog.tex
TEX += bib/bib.tex

LST  = frames/frame.py 
LST += frames/prim.py frames/string.py frames/symbol.py frames/number.py
LST += frames/stack.py frames/dict.py frames/container.py
LST += forth/parser.py forth/lexer.py

LATEX = pdflatex -halt-on-error

book.pdf: $(TEX) $(LST) $(FIG)
	$(LATEX) $< && $(LATEX) $<

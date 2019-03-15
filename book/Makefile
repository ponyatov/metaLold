TEX  = hico.tex header.tex

TEX += intro/intro.tex intro/denial.tex intro/meta.tex 
TEX += intro/brooks.tex intro/lop.tex intro/homoiconic.tex

TEX += first/steps.tex first/eds.tex first/whitebox.tex first/install.tex

TEX += frames/frames.tex frames/frame.tex frames/dump.tex
TEX += frames/prim.tex frames/string.tex frames/symbol.tex frames/number.tex
TEX += frames/container.tex frames/stack.tex frames/dict.tex

TEX += forth/forth.tex forth/dict.tex forth/ply.tex forth/repl.tex
TEX += forth/cmdline.tex
TEX += web/web.tex
TEX += dyna/dyna.tex dyna/llvm.tex dyna/managed.tex
TEX += prolog/prolog.tex

TEX += meta/circ.tex
LST += meta/ebldfiles.ini meta/eclfiles.ini meta/files.ini
LST += meta/header.ini meta/vimfiles.ini

TEX += mcu/mcu.tex mcu/ardu/ino.tex mcu/msp/msp.tex mcu/arm/cortex.tex
TEX += linux/linux.tex event/event.tex

TEX += code/in.tex code/emcin.tex

TEX += os/os.tex os/boot.tex os/sched.tex os/files.tex
TEX += os/net.tex os/user.tex os/gui.tex

FIG += mcu/ardu/micro.png mcu/ardu/uno.jpg mcu/ardu/nano.jpg

TEX += bib/bib.tex

LST  = frames/frame.py 
LST += frames/prim.py frames/string.py frames/symbol.py frames/number.py
LST += frames/stack.py frames/dict.py frames/container.py
LST += forth/parser.py forth/lexer.py forth/inter.py forth/repl.py
LST += forth/cmdline.py

LATEX = pdflatex -halt-on-error

book.pdf: $(TEX) $(LST) $(FIG)
	$(LATEX) $< && $(LATEX) $<

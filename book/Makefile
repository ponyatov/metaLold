TEX  = metaL.tex header.tex

TEX += intro/intro.tex intro/denial.tex intro/meta.tex 
TEX += intro/brooks.tex intro/lop.tex intro/homoiconic.tex

TEX += first/steps.tex first/eds.tex first/whitebox.tex first/install.tex

TEX += frames/frames.tex frames/frame.tex frames/dump.tex
TEX += frames/prim.tex frames/string.tex frames/symbol.tex frames/number.tex
TEX += frames/container.tex frames/stack.tex frames/dict.tex
TEX += frames/active.tex

TEX += forth/forth.tex forth/dict.tex forth/ply.tex forth/repl.tex
TEX += forth/cmdline.tex

TEX += web/web.tex
TEX += web/templ.tex 
LST += web/templ.css web/templ.html web/templ.py
TEX += web/form.tex
LST += web/form.py web/form.css web/form.html
TEX += web/dump.tex
LST += web/dump.html web/dump.css web/dump.py
TEX += web/viz.tex
LST += web/viz.html web/viz.css web/viz.py
TEX += web/google.tex
LST += ../appengine_config.py ../requirements.txt
TEX += web/wasm/wasm.tex

TEX += dyna/dyna.tex dyna/llvm.tex dyna/managed.tex

TEX += cpp/cpp.tex cpp/gc.tex

TEX += prolog/prolog.tex

TEX += syntax/syntax.tex syntax/ragel/ragel.tex syntax/ragel/java.tex
LST += syntax/ragel/java??.*
TEX += syntax/ply/ply.tex
LST += syntax/ply/lex.py syntax/ply/yacc.py

TEX += meta/circ.tex
LST += meta/ebldfiles.ini meta/eclfiles.ini meta/files.ini
LST += meta/header.ini meta/vimfiles.ini

TEX += meta/ouro/boros.tex meta/ouro/files.tex
FIG += meta/ouro/boros.png

TEX += mcu/mcu.tex mcu/ardu/ino.tex mcu/msp/msp.tex
TEX += mcu/arm/cortex.tex mcu/arm/setup.tex

TEX += mcu/parse/ragel.tex mcu/parse/bin.tex

TEX += mcu/arm/cortex.tex mcu/gnu/gcc.tex 
FIG += /tmp/gnugcc.pdf
TEX += mcu/arm/f030.tex
FIG += mcu/arm/pinout.png mcu/arm/HSE.png mcu/arm/HPclock.png

TEX += linux/linux.tex event/event.tex

TEX += code/in.tex code/emcin.tex code/cpp.tex code/ide.tex code/literate.tex

TEX += concept/concept.tex

TEX += gui/wx.tex
LST += gui/wx00.py gui/wx01.py gui/wx02.py
LST += gui/wx03.py gui/wx04.py gui/wx05.py gui/wx06.py
LST += gui/wx07.py gui/wx08.py gui/wx09.py gui/wx10.py
LST += gui/wx11.py gui/wx12.py gui/wx13.py gui/wx14.py
LST += gui/wx15.py gui/wx16.py gui/wx17.py gui/wx18.py
FIG += gui/wx00.png gui/wx01.png gui/wx02.png

TEX += os/os.tex os/boot.tex os/sched.tex os/files.tex
TEX += os/net.tex os/user.tex os/gui.tex

TEX += game/dev.tex game/cross.tex game/boot.tex game/video.tex
LST += game/cross0.mk game/boot00.mk game/boot00.objdump
TEX += game/debug.tex
LST += game/debug0.mk game/debug1.mk
FIG += game/debug1A.png game/debug1B.png game/debug1C.png /tmp/debug.pdf

FIG += mcu/ardu/micro.png mcu/ardu/uno.jpg mcu/ardu/nano.jpg

TEX += android/android.tex

TEX += py/py.tex
LST += py/hello*.py

TEX += docu/ment.tex

TEX += bib/bib.tex

LST += frames/frame.py 
LST += frames/prim.py frames/string.py frames/symbol.py frames/number.py
LST += frames/stack.py frames/dict.py frames/container.py
LST += forth/parser.py forth/lexer.py forth/inter.py forth/repl.py
LST += forth/cmdline.py

LATEX = pdflatex -halt-on-error

metaL.pdf: $(TEX) $(LST) $(FIG)
	$(LATEX) $< && $(LATEX) $<

/tmp/%.pdf: mcu/%.dot
	dot -T pdf -o /tmp/crop.pdf $< && pdfcrop /tmp/crop.pdf $@

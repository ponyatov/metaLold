CPU     = i386
CFG_CPU = --with-cpu=$(CPU) --with-float=soft
TARGET  = $(CPU)-elf
CROSS   = $(CURDIR)/$(TARGET)/bin

cross: ../mcu/Makefile
	make -f $< \
		TARGET=$(TARGET) CFG_CPU="$(CFG_CPU)" \
			dirs gz cclibs binutils gcc0
CPU     = i386
TARGET  = $(CPU)-elf
CFG_CPU = --with-cpu=$(CPU) --with-float=soft
CROSS   = $(CURDIR)/$(TARGET)/bin
QEMU	= qemu-system-i386

cross: ../mcu/Makefile
	make -f $< \
		TARGET=$(TARGET) CFG_CPU="$(CFG_CPU)" cross0
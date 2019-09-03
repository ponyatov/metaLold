CPU     = i386
TARGET  = $(CPU)-elf
CFG_CPU = --with-cpu=$(CPU)
CROSS   = $(CURDIR)/$(TARGET)/bin

cross: ../mcu/Makefile
	make -f $< \
		TARGET=$(TARGET) CFG_CPU="$(CFG_CPU)" cross0

CPU     = i386
CFG_CPU = --with-cpu=$(CPU) --with-float=soft
TARGET  = $(CPU)-elf
CROSS   = $(CURDIR)/$(TARGET)/bin
QEMU	= qemu-system-i386

go: game.elf
	echo Ctrl-A C
	$(QEMU) -kernel $< -nographic -s -S

cross: ../mcu/Makefile
	make -f $< TARGET=$(TARGET) CFG_CPU="$(CFG_CPU)" dirs gz cclibs binutils gcc0

C = multiboot.S
H = multiboot.h

GCC = $(CROSS)/$(TARGET)-gcc
CFLAGS = -march=$(CPU) -mtune=$(CPU) -m32 -I$(CURDIR)

LD = $(CROSS)/$(TARGET)-ld
LDFLAGS = -m elf_i386 -T multiboot.ld

OBJDUMP = LANG=C $(CROSS)/$(TARGET)-objdump

game.elf: multiboot.o
	$(LD) $(LDFLAGS) -o $@ $^
	$(OBJDUMP) -x -d $@ > $@.objdump

multiboot.o: multiboot.S multiboot.h Makefile
	$(GCC) $(CFLAGS) -c -o $@ $<
	$(OBJDUMP) -x -d $@ > $@.objdump
	

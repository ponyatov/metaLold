
C = multiboot.S
H = multiboot.h

GCC = gcc
CFLAGS = -march=i386 -mtune=i386 -m32 -I$(CURDIR)

LD = ld
LDFLAGS = -melf_i386 -Tmultiboot.ld

game.elf: multiboot.o
	$(LD) $(LDFLAGS) -o $@ $^
	LANG=C objdump -x -d $@ > $@.objdump

multiboot.o: multiboot.S multiboot.h Makefile
	$(GCC) $(CFLAGS) -c -o $@ $<
	LANG=C objdump -x -d $@ > $@.objdump
	
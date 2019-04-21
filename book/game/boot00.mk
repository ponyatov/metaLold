GCC = gcc
CFLAGS = -march=i386 -mtune=i386 -m32 -I$(CURDIR)

multiboot.o: multiboot.S multiboot.h Makefile
	$(GCC) $(CFLAGS) -c -o $@ $< &&\
	objdump -x $@ > $@.objdump
	
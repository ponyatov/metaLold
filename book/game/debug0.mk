QEMU	= qemu-system-i386
GDB		= $(CROSS)/$(TARGET)-gdb

go: game.elf
	$(QEMU) -kernel $< -nographic -s -S &
	$(GDB) -x $<.gdb $<

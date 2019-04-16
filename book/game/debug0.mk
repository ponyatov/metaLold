QEMU	= qemu-system-i386
GDB		= $(CROSS)/$(TARGET)-gdb
CFLAGS += -g2

go: game.elf
	# exit from QEMU: [Ctrl-A] [X]
	$(QEMU) -kernel $< -nographic -s -S &
	$(GDB) -x $<.gdb $< ; killall $(QEMU)

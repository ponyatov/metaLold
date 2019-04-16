QEMU	= qemu-system-i386

go: game.elf
	echo Ctrl-A C
	$(QEMU) -kernel $< -nographic -s -S
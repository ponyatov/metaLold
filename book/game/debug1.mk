DDD		= "$(GDB) -x $<.gdb $< ; killall $(QEMU)"

go: game.elf
	# exit from QEMU: [Ctrl-A] [X]
	$(QEMU) -kernel $< -nographic -s -S &
	ddd --debugger $(DDD)
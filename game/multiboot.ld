OUTPUT_FORMAT(elf32-i386)

MEMORY {
	RAM    : ORIGIN = 1M      , LENGTH = 64M
	SCREEN : ORIGIN = 0xB8000 , LENGTH = 80*25*2
	VESA   : ORIGIN = 0xA0000 , LENGTH = 1024*768*3
}

SECTIONS {

	.text   : { *(.multiboot) *(.text) } >RAM
	_etext  = . ;
	
	_data   = . ;
	.data   : { *(.data)			   } >RAM
	_edata  = . ;
	
	_bstart = . ;
	.bss	: { *(.bss)  *(COMMON) 	   } >RAM
	_bend   = . ;
	
	_edata  = . ;
	_end	= . ;
	
	_stack  = . ;
	.stack  : { *(.stack)   		   } >RAM
	_estack = . ;
	 
	.screen : { *(.screen)			   } >SCREEN
	.vesa   : { *(.vesa)			   } >VESA
}

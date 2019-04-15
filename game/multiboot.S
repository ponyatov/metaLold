#define  ASM
#include <multiboot.h>

	.section .multiboot
_start:
	jmp _init

	.align  4
multiboot_header:
	.long   MULTIBOOT_HEADER_MAGIC
	.long   MULTIBOOT_HEADER_FLAGS
	.long   -(MULTIBOOT_HEADER_MAGIC + MULTIBOOT_HEADER_FLAGS)
	.long   multiboot_header
	.long   _start
	.long   _edata
	.long   _end
	.long   _init

_init:

	/* init stack pointer */
	movl    $(_stack + STACK_SIZE), %esp
	/* reset EFLAGS */
	pushl   $0
	popf
	/* mutiboot info structure */
	pushl   %ebx
	/* push magic value */
	pushl   %eax

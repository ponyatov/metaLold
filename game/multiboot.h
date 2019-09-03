/* Multiboot1 spec */

/* http://www.gnu.org/software/grub/manual/multiboot/multiboot.html */

#ifndef _H_MULTIBOOT
#define _H_MULTIBOOT

#define MULTIBOOT_HEADER_MAGIC		0x1BADB002
#define MULTIBOOT_HEADER_FLAGS		0x00000003
#define MULTIBOOT_BOOTLOADER_MAGIC	0x2BADB002

#define STACK_SIZE                      0x4000

#ifndef ASM

/* The Multiboot header. */
typedef struct multiboot_header
{
	uint32_t magic;
	uint32_t flags;
	uint32_t checksum;
	uint32_t header_addr;
	uint32_t load_addr;
	uint32_t load_end_addr;
	uint32_t bss_end_addr;
	uint32_t entry_addr;
} multiboot_header_t;

#endif // ASM

#endif // _H_MULTIBOOT

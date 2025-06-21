; src/gdt.asm
[BITS 32]
section .text
global gdt_flush

gdt_flush:
    lgdt [esp+4]
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    ret

; src/gdt.asm
[BITS 32]
section .data
align 8
GDT:
    dq 0x0000000000000000        ; null
    dq 0x00cf9a000000ffff        ; code segment
    dq 0x00cf92000000ffff        ; data segment
GDT_end:

gdt_ptr:
    dw GDT_end - GDT - 1
    dd GDT

section .text
global gdt_install

gdt_install:
    lgdt [gdt_ptr]
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    jmp 0x08:flush
flush:
    ret

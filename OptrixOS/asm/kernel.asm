[BITS 16]
[ORG 0x1000]

%include "shell.asm"

kernel_start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    call shell_start

.halt:
    hlt
    jmp .halt

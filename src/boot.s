BITS 32
section .multiboot
    dd 0x1BADB002
    dd 0
    dd -(0x1BADB002 + 0)

section .text
extern kernel_main
    global _start
_start:
    cli
    mov esp, stack_top
    call kernel_main
.hang:
    hlt
    jmp .hang

section .bss
    align 16
stack_bottom:
    resb 16384
stack_top:

BITS 32
section .text
extern kernel_main
    global _start
_start:
    cli
    mov esp, stack_top
    push edi
    push esi
    call kernel_main
.hang:
    hlt
    jmp .hang

section .bss
    align 16
stack_bottom:
    resb 16384
stack_top:

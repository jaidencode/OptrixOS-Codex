[bits 16]
[org 0x7C00]

%ifndef KERNEL_SECTORS
%define KERNEL_SECTORS 1
%endif

%ifndef KERNEL_LBA
%define KERNEL_LBA 1
%endif

%ifndef KERNEL_LOAD_ADDR
%define KERNEL_LOAD_ADDR 0x00100000
%endif

start:
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov [BOOT_DRIVE], dl

    ; set up disk address packet
    mov word [dap+2], KERNEL_SECTORS
    mov dword [dap+4], KERNEL_LOAD_ADDR
    mov dword [dap+8], KERNEL_LBA
    mov dword [dap+12], 0

    mov si, dap
    mov dl, [BOOT_DRIVE]
    mov ah, 0x42
    int 0x13
    jc disk_error

    call enable_a20

    cli
    lgdt [gdt_desc]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp CODE_SEL:protected

[bits 32]
protected:
    mov ax, DATA_SEL
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000
    mov eax, KERNEL_LOAD_ADDR
    jmp eax

[bits 16]
disk_error:
    cli
    hlt
    jmp disk_error

enable_a20:
    in al, 0x92
    or al, 2
    out 0x92, al
    ret

; GDT with null, code, data
ALIGN 4
gdt_start:
    dq 0
gdt_code:
    dw 0xFFFF
    dw 0
    db 0
    db 0x9A
    db 0xCF
    db 0
gdt_data:
    dw 0xFFFF
    dw 0
    db 0
    db 0x92
    db 0xCF
    db 0
gdt_end:

gdt_desc:
    dw gdt_end - gdt_start - 1
    dd gdt_start

CODE_SEL equ 0x08
DATA_SEL equ 0x10

BOOT_DRIVE db 0

dap:
    db 0x10,0      ; size and reserved
    dw 0           ; sectors (patched)
    dd KERNEL_LOAD_ADDR ; load address
    dq KERNEL_LBA      ; starting LBA

TIMES 510-($-$$) db 0
DW 0xAA55

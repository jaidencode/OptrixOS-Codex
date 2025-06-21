[BITS 16]
[ORG 0x7E00]

%ifndef KERNEL_LOAD_ADDR
%define KERNEL_LOAD_ADDR 0x1000
%endif
%ifndef KERNEL_START_SECTOR
%define KERNEL_START_SECTOR 2
%endif
%ifndef KERNEL_SECTORS
%define KERNEL_SECTORS 1
%endif

stage2_start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7E00

    mov si, stage2_banner
    call print

    mov [boot_drive], dl

    mov si, load_kernel_msg
    call print

    ; load kernel
    mov bx, KERNEL_LOAD_ADDR
    mov dh, 0
    mov dl, [boot_drive]
    mov ah, 0x02
    mov al, KERNEL_SECTORS
    mov ch, 0
    mov cl, KERNEL_START_SECTOR
    int 0x13
    jc disk_error

    mov si, jump_kernel_msg
    call print

    mov dl, [boot_drive]
    jmp 0x0000:KERNEL_LOAD_ADDR

disk_error:
    mov si, err_msg
    call print
    jmp $

print:
    mov ah, 0x0E
.next:
    lodsb
    test al, al
    jz .done
    int 0x10
    jmp .next
.done:
    ret

boot_drive db 0
err_msg db 'Stage2 error',0
stage2_banner db 'Stage2 start',13,10,0
load_kernel_msg db 'Loading kernel...',13,10,0
jump_kernel_msg db 'Jumping to kernel',13,10,13,10,0

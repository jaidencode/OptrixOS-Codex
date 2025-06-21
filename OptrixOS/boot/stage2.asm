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

    mov [boot_drive], dl

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

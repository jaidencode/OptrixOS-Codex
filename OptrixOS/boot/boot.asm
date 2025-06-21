[BITS 16]
[ORG 0x7C00]

boot_start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    ; show basic BIOS banner
    mov si, bios_banner
    call print

    mov [boot_drive], dl

    mov si, load_stage2_msg
    call print

    ; Read stage2 from disk
    mov bx, 0x7E00          ; load address
    mov dh, 0               ; head
    mov dl, [boot_drive]
    mov ah, 0x02            ; read sectors
    mov al, STAGE2_SECTORS
    mov ch, 0
    mov cl, 2               ; starting sector 2
    int 0x13
    jc disk_error

    mov si, jump_stage2_msg
    call print

    jmp 0x0000:0x7E00

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
err_msg db 'Boot error',0
bios_banner db 'Optrix BIOS v0.1',13,10,0
load_stage2_msg db 'Loading stage2...',13,10,0
jump_stage2_msg db 'Jumping to stage2',13,10,13,10,0

times 510-($-$$) db 0
DW 0xAA55

; boot/boot.asm
BITS 16
ORG 0x7C00

start:
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov si, msg_loading
    call print_string

    mov bx, 0x1000         ; load segment for stage2
    mov dh, 2              ; sectors to read
    call load_stage2

    jmp 0x1000:0           ; jump to stage2

hang:   jmp hang

; -- print_string --
print_string:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0E
    int 0x10
    jmp print_string
.done:
    ret

msg_loading db 'Loading DreamOS...', 0

; -- load_stage2 --
load_stage2:
    pusha
    mov ah, 0x02           ; BIOS read sectors
    mov al, dh
    mov ch, 0
    mov cl, 2
    mov dh, 0
    mov dl, 0x00
    mov es, bx
    mov bx, 0x0000
    int 0x13
    jc hang
    popa
    ret

TIMES 510-($-$$) db 0
DW 0xAA55

[BITS 16]

; Print character in AL at current cursor position using BIOS
vid_putc:
    mov ah, 0x0E
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    ret

; Print null-terminated string at DS:SI
vid_print:
    push ax
.print_loop:
    lodsb
    or al, al
    jz .done
    call vid_putc
    jmp .print_loop
.done:
    pop ax
    ret

; Output CRLF
vid_newline:
    push ax
    mov al, 0x0D
    call vid_putc
    mov al, 0x0A
    call vid_putc
    pop ax
    ret

; Clear screen and reset cursor
vid_clear:
    mov ax, 0x0600
    mov bh, 0x07
    mov cx, 0
    mov dx, 0x184F
    int 0x10
    mov ah, 0x02
    mov bh, 0
    mov dh, 0
    mov dl, 0
    int 0x10
    ret

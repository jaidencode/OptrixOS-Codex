[BITS 16]
[ORG 0x1000]

kernel_start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax

    mov ax, 0xB800
    mov es, ax

    mov di, 0
    mov cx, 80*25
    mov ax, 0x1F20        ; white on blue space
.fill:
    mov [es:di], ax
    add di, 2
    loop .fill

    ; reset cursor to 0,0
    mov dx, 0x3D4
    mov al, 0x0F
    out dx, al
    inc dx
    xor al, al
    out dx, al
    mov dx, 0x3D4
    mov al, 0x0E
    out dx, al
    inc dx
    xor al, al
    out dx, al


    ; print kernel message on first line
    mov di, 0
    mov si, kernel_msg
    call print_string

    ; print BIOS information on second line
    mov di, 160          ; start of line 2
    mov si, bios_label
    call print_string

    ; boot drive passed in DL from stage2
    mov al, dl
    call print_hex8

    mov si, mem_label
    call print_string

    int 0x12              ; AX = base memory in KB
    call print_hex16
    mov si, kb_suffix
    call print_string

.halt:
    hlt
    jmp .halt

; --- Printing routines ---
print_string:
.ps_next:
    lodsb
    or al, al
    jz .ps_done
    mov ah, 0x1F
    mov [es:di], ax
    add di, 2
    jmp .ps_next
.ps_done:
    ret

hex_digit:
    cmp al, 10
    jb .hd_num
    add al, 'A' - 10
    jmp .hd_store
.hd_num:
    add al, '0'
.hd_store:
    mov ah, 0x1F
    mov [es:di], ax
    add di, 2
    ret

print_hex8:
    push ax
    mov bh, al
    mov al, bh
    shr al, 4
    call hex_digit
    mov al, bh
    and al, 0x0F
    call hex_digit
    pop ax
    ret

print_hex16:
    push ax
    mov bx, ax
    mov al, bh
    shr al, 4
    call hex_digit
    mov al, bh
    and al, 0x0F
    call hex_digit
    mov al, bl
    shr al, 4
    call hex_digit
    mov al, bl
    and al, 0x0F
    call hex_digit
    pop ax
    ret

kernel_msg db 'OptrixOS Kernel Loaded',0
bios_label db 'BIOS Drive: 0x',0
mem_label db ' Memory: 0x',0
kb_suffix db ' KB',0

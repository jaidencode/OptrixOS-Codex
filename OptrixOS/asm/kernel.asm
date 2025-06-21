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

    mov si, message
    mov di, 0
.print:
    lodsb
    or al, al
    jz .halt
    mov ah, 0x1F
    mov [es:di], ax
    add di, 2
    jmp .print

.halt:
    hlt
    jmp .halt

message db 'Welcome to OptrixOS',0

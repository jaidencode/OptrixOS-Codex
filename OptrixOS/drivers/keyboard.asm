[BITS 16]

; Wait for a key press and return ASCII in AL
kbd_getch:
    mov ah, 0x00
    int 0x16
    ret

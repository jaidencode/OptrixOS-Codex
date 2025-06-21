; boot/stage2.asm
BITS 16
ORG 0x1000

start:
    cli
    lgdt [gdt_ptr]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp 0x08:start_pm

gdt_start:
    dq 0x0000000000000000
    dq 0x00cf9a000000ffff
    dq 0x00cf92000000ffff
gdt_end:

gdt_ptr:
    dw gdt_end - gdt_start - 1
    dd gdt_start

BITS 32
start_pm:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000

    mov esi, msg
    call print_string_pm

    ; Load kernel (sectors 4+, 10 sectors = 20K)
    mov eax, 0x0000
    mov dl, 0x00
    mov dh, 10
    mov cx, 4
    mov edi, 0x10000
load_kernel:
    pusha
    mov ah, 0x02
    mov al, dh
    mov ch, 0
    mov cl, cl
    mov dh, 0
    mov dl, 0x00
    mov bx, di
    int 0x13
    popa

    ; jump to kernel
    jmp 0x10000

; Print string in protected mode (BIOS video memory write)
print_string_pm:
    mov ah, 0x0F
    mov bh, 0x00
.next:
    lodsb
    test al, al
    jz .done
    mov [0xb8000], al
    add dword [0xb8000], 2
    jmp .next
.done:
    ret

msg db 'DreamOS Kernel...', 0

times 2048-($-$$) db 0

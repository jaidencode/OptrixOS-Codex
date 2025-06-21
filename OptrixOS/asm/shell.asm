[BITS 16]

%include "../drivers/keyboard.asm"
%include "../drivers/video.asm"

path_current db 'root/',0
prompt_suffix db '> ',0
welcome_msg db 'Welcome to OptrixOS Shell',0
help_msg db 'Available commands: help, clear, echo',0
unknown_msg db 'Unknown command',0

str_help db 'help',0
str_clear db 'clear',0
str_echo db 'echo ',0

input_buf times 128 db 0

; Read a line into input_buf, result in input_buf
input_line:
    mov di, input_buf
    xor cx, cx
.read:
    call kbd_getch
    cmp al, 13
    je .done
    cmp al, 8
    je .backspace
    call vid_putc
    stosb
    inc cx
    cmp cx, 126
    jb .read
    jmp .read
.backspace:
    cmp cx, 0
    je .read
    dec di
    dec cx
    mov al, 8
    call vid_putc
    mov al, ' '
    call vid_putc
    mov al, 8
    call vid_putc
    jmp .read
.done:
    call vid_newline
    mov al, 0
    stosb
    ret

; Compare strings DS:SI and DS:DI, set AL=0 if equal
strcmp:
    push si
    push di
.loop:
    lodsb
    mov bl, [di]
    inc di
    cmp al, bl
    jne .noteq
    or al, al
    jne .loop
    mov al, 0
    jmp .finish
.noteq:
    mov al, 1
.finish:
    pop di
    pop si
    ret

; Check if input starts with 'echo '
check_echo:
    push si
    push di
    mov si, input_buf
    mov di, str_echo
    mov cx, 5
.loop_e:
    lodsb
    mov bl, [di]
    inc di
    cmp al, bl
    jne .noteq_e
    loop .loop_e
    mov al, 0
    jmp .end_e
.noteq_e:
    mov al, 1
.end_e:
    pop di
    pop si
    ret

shell_start:
    call vid_clear
    mov si, welcome_msg
    call vid_print
    call vid_newline

.shell_loop:
    mov al, '$'
    call vid_putc
    mov si, path_current
    call vid_print
    mov si, prompt_suffix
    call vid_print

    call input_line

    mov si, input_buf
    mov di, str_help
    call strcmp
    cmp al, 0
    je .do_help

    mov si, input_buf
    mov di, str_clear
    call strcmp
    cmp al, 0
    je .do_clear

    call check_echo
    cmp al, 0
    je .do_echo

    mov si, unknown_msg
    call vid_print
    call vid_newline
    jmp .shell_loop

.do_help:
    mov si, help_msg
    call vid_print
    call vid_newline
    jmp .shell_loop

.do_clear:
    call vid_clear
    jmp .shell_loop

.do_echo:
    mov si, input_buf + 5
    call vid_print
    call vid_newline
    jmp .shell_loop

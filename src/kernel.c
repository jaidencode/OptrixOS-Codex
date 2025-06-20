#include <stddef.h>
#include <stdint.h>
#include "fs/vfs.h"
#include "string.h"

static volatile unsigned char *video = (unsigned char *)0xb8000;
static unsigned short cursor = 0;
static const unsigned char ATTR = 0x1F; /* white on blue */
static char current_path[64] = "root";
static char drive_letter = 'C';

static inline void outb(uint16_t port, uint8_t val) {
    __asm__ volatile ("outb %0, %1" : : "a"(val), "Nd"(port));
}

static inline uint8_t inb(uint16_t port) {
    uint8_t ret;
    __asm__ volatile ("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}

static void print_char(char c) {
    if (c == '\n') {
        cursor = (cursor / 80 + 1) * 80;
        return;
    }
    video[cursor * 2] = c;
    video[cursor * 2 + 1] = ATTR;
    cursor++;
}

static void print_string(const char *s) {
    for (size_t i = 0; s[i]; i++)
        print_char(s[i]);
}

static void backspace(void) {
    if (cursor > 0) {
        cursor--;
        video[cursor * 2] = ' ';
        video[cursor * 2 + 1] = ATTR;
    }
}

static void clear_screen(void) {
    for (unsigned int i = 0; i < 80 * 25; i++) {
        video[i * 2] = ' ';
        video[i * 2 + 1] = ATTR;
    }
    cursor = 0;
}

static const char keymap[128] = {
    0, 27, '1','2','3','4','5','6','7','8','9','0','-','=', '\b',
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n',0,
    'a','s','d','f','g','h','j','k','l',';','\'', '`',0,'\\',
    'z','x','c','v','b','n','m',',','.','/',0,'*',0,' ',0,
};

static unsigned char get_scancode(void) {
    while ((inb(0x64) & 1) == 0)
        ;
    return inb(0x60);
}

static void read_line(char *buf, size_t max) {
    size_t idx = 0;
    for (;;) {
        unsigned char sc = get_scancode();
        if (sc & 0x80)  /* ignore releases */
            continue;
        if (sc == 0x1C) { /* Enter */
            print_char('\n');
            buf[idx] = 0;
            return;
        } else if (sc == 0x0E) { /* Backspace */
            if (idx > 0) {
                idx--;
                backspace();
            }
        } else {
            char c = keymap[sc];
            if (c && idx + 1 < max) {
                buf[idx++] = c;
                print_char(c);
            }
        }
    }
}

static void set_path(const char *p) {
    size_t i = 0;
    while (p[i] && i < sizeof(current_path) - 1) {
        current_path[i] = p[i];
        i++;
    }
    current_path[i] = 0;
}

static void list_printer(const char *name) {
    print_string(name);
    print_char('\n');
}

static void shell(void) {
    char line[80];
    for (;;) {
        print_char(drive_letter);
        print_string(":\\");
        print_string(current_path);
        print_string("> ");
        read_line(line, sizeof(line));

        if (strcmp(line, "help") == 0) {
            print_string("Commands: help, cd, ls, cat, write, format, halt\n");
        } else if (strncmp(line, "cd ", 3) == 0) {
            set_path(line + 3);
        } else if (strcmp(line, "ls") == 0) {
            vfs_list(list_printer);
        } else if (strncmp(line, "cat ", 4) == 0) {
            char buf[512];
            int r = vfs_read(line + 4, buf, sizeof(buf) - 1);
            if (r < 0) {
                print_string("File not found\n");
            } else {
                buf[r] = 0;
                print_string(buf);
                print_char('\n');
            }
        } else if (strncmp(line, "write ", 6) == 0) {
            char *rest = line + 6;
            char *sp = strchr(rest, ' ');
            if (sp) {
                *sp = 0;
                vfs_write(rest, sp + 1, strlen(sp + 1));
            }
        } else if (strcmp(line, "format") == 0) {
            vfs_format();
            print_string("Disk formatted\n");
        } else if (strcmp(line, "halt") == 0) {
            break;
        } else if (line[0]) {
            print_string("Unknown command\n");
        }
    }
    for (;;) {
        __asm__("hlt");
    }
}

void kernel_main(void) {
    clear_screen();
    print_string("OptrixOS booted\n");
    vfs_init();
    vfs_mount(FS_EXT2);
    vfs_format();
    shell();
}

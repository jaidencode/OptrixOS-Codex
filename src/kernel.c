#include <stddef.h>
#include <stdint.h>
#include "fs/vfs.h"
#include "fs/ext2.h"
#include "string.h"
#include "shell.h"

static volatile unsigned char *video = (unsigned char *)0xb8000;
static unsigned short cursor = 0;
static const unsigned char ATTR = 0x1F; /* white on blue */

static inline void outb(uint16_t port, uint8_t val) {
    __asm__ volatile ("outb %0, %1" : : "a"(val), "Nd"(port));
}

static inline uint8_t inb(uint16_t port) {
    uint8_t ret;
    __asm__ volatile ("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}

void print_char(char c) {
    if (c == '\n') {
        cursor = (cursor / 80 + 1) * 80;
        return;
    }
    video[cursor * 2] = c;
    video[cursor * 2 + 1] = ATTR;
    cursor++;
}

void print_string(const char *s) {
    for (size_t i = 0; s[i]; i++)
        print_char(s[i]);
}

void backspace(void) {
    if (cursor > 0) {
        cursor--;
        video[cursor * 2] = ' ';
        video[cursor * 2 + 1] = ATTR;
    }
}

void clear_screen(void) {
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

unsigned char get_scancode(void) {
    while ((inb(0x64) & 1) == 0)
        ;
    return inb(0x60);
}

void read_line(char *buf, size_t max) {
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


void kernel_main(void *rootfs, unsigned long rootfs_size) {
    clear_screen();
    print_string("OptrixOS booted\n");
    vfs_init();
    vfs_mount(FS_EXT2);
    ext2_load(rootfs, rootfs_size);
    shell_run();
}

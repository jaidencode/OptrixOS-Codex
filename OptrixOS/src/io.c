#include "io.h"

static unsigned short *vidmem = (unsigned short *)0xB8000;
static unsigned short cursor = 0;

void outb(unsigned short port, unsigned char val) {
    asm volatile ("outb %0, %1" : : "a"(val), "Nd"(port));
}
unsigned char inb(unsigned short port) {
    unsigned char ret;
    asm volatile ("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}
void clear_screen() {
    for (int i = 0; i < 80 * 25; i++)
        vidmem[i] = 0x0720;
    cursor = 0;
}
void print(const char* str) {
    while (*str) {
        if (*str == '\n') {
            cursor += 80 - (cursor % 80);
        } else {
            vidmem[cursor++] = 0x0700 | *str;
        }
        if (cursor >= 80 * 25) cursor = 0;
        str++;
    }
}

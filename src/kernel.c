#include <stddef.h>

static volatile unsigned char *video = (unsigned char *)0xb8000;

void kernel_main(void) {
    const char *msg = "Hello from OptrixOS";
    for (size_t i = 0; msg[i]; i++) {
        video[i * 2] = msg[i];
        video[i * 2 + 1] = 0x07;
    }
    for (;;) {
        __asm__("hlt");
    }
}

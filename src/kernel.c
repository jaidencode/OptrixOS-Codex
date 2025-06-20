#include <stddef.h>
#include "fs/vfs.h"

static volatile unsigned char *video = (unsigned char *)0xb8000;

void kernel_main(void) {
    const char *msg = "Hello from OptrixOS";
    for (size_t i = 0; msg[i]; i++) {
        video[i * 2] = msg[i];
        video[i * 2 + 1] = 0x07;
    }
    vfs_init();
    vfs_mount(FS_EXT2);

    for (;;) {
        __asm__("hlt");
    }
}

#include "ext2.h"
#include <stddef.h>

void ext2_init(void) {
    /* TODO: initialize ext2 driver */
}

int ext2_read(const char *path, void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: read from ext2 */
    return -1;
}

int ext2_write(const char *path, const void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: write to ext2 */
    return -1;
}

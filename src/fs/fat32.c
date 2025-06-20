#include "fat32.h"
#include <stddef.h>

void fat32_init(void) {
    /* TODO: initialize FAT32 driver */
}

int fat32_read(const char *path, void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: read from FAT32 */
    return -1;
}

int fat32_write(const char *path, const void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: write to FAT32 */
    return -1;
}

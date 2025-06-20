#include "ntfs.h"
#include <stddef.h>

void ntfs_init(void) {
    /* TODO: initialize NTFS driver */
}

int ntfs_read(const char *path, void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: read from NTFS */
    return -1;
}

int ntfs_write(const char *path, const void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: write to NTFS */
    return -1;
}

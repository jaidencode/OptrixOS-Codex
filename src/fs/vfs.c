#include "vfs.h"
#include <stddef.h>

void vfs_init(void) {
    /* Initialize VFS structures. */
}

int vfs_mount(fs_type_t type) {
    (void)type; /* unused */
    /* TODO: mount appropriate file system driver */
    return 0;
}

int vfs_read(const char *path, void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: dispatch read to proper FS driver */
    return -1;
}

int vfs_write(const char *path, const void *buf, unsigned long len) {
    (void)path; (void)buf; (void)len;
    /* TODO: dispatch write to proper FS driver */
    return -1;
}

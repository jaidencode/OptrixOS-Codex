#include "vfs.h"
#include "ext2.h"
#include "fat32.h"
#include "ntfs.h"
#include "../string.h"

typedef struct {
    int (*read)(const char *, void *, unsigned long);
    int (*write)(const char *, const void *, unsigned long);
} driver_t;

static driver_t driver;

void vfs_init(void) {
    memset(&driver, 0, sizeof(driver));
}

int vfs_mount(fs_type_t type) {
    switch (type) {
    case FS_EXT2:
        ext2_init();
        driver.read = ext2_read;
        driver.write = ext2_write;
        break;
    case FS_FAT32:
        fat32_init();
        driver.read = fat32_read;
        driver.write = fat32_write;
        break;
    case FS_NTFS:
        ntfs_init();
        driver.read = ntfs_read;
        driver.write = ntfs_write;
        break;
    default:
        return -1;
    }
    return 0;
}

int vfs_read(const char *path, void *buf, unsigned long len) {
    if (!driver.read)
        return -1;
    return driver.read(path, buf, len);
}

int vfs_write(const char *path, const void *buf, unsigned long len) {
    if (!driver.write)
        return -1;
    return driver.write(path, buf, len);
}

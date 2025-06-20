#include "vfs.h"
#include "ext2.h"
#include "fat32.h"
#include "ntfs.h"
#include "../string.h"

typedef struct {
    int (*read)(const char *, void *, unsigned long);
    int (*write)(const char *, const void *, unsigned long);
    void (*list)(void (*cb)(const char *name));
    void (*format)(void);
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
        driver.list = ext2_list;
        driver.format = ext2_format;
        break;
    case FS_FAT32:
        fat32_init();
        driver.read = fat32_read;
        driver.write = fat32_write;
        driver.list = fat32_list;
        driver.format = fat32_format;
        break;
    case FS_NTFS:
        ntfs_init();
        driver.read = ntfs_read;
        driver.write = ntfs_write;
        driver.list = ntfs_list;
        driver.format = ntfs_format;
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

void vfs_format(void) {
    if (driver.format)
        driver.format();
}

void vfs_list(void (*cb)(const char *name)) {
    if (driver.list)
        driver.list(cb);
}

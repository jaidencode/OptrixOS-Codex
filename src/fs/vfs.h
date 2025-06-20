#ifndef VFS_H
#define VFS_H

typedef enum {
    FS_EXT2,
    FS_FAT32,
    FS_NTFS
} fs_type_t;

void vfs_init(void);
int vfs_mount(fs_type_t type);
int vfs_read(const char *path, void *buf, unsigned long len);
int vfs_write(const char *path, const void *buf, unsigned long len);

#endif // VFS_H

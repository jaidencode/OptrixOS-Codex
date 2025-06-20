#ifndef NTFS_H
#define NTFS_H

void ntfs_init(void);
int ntfs_read(const char *path, void *buf, unsigned long len);
int ntfs_write(const char *path, const void *buf, unsigned long len);

#endif // NTFS_H

#ifndef NTFS_H
#define NTFS_H

void ntfs_init(void);
void ntfs_format(void);
void ntfs_list(void (*cb)(const char *name));
int ntfs_read(const char *path, void *buf, unsigned long len);
int ntfs_write(const char *path, const void *buf, unsigned long len);

#endif // NTFS_H

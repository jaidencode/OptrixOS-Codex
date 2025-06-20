#ifndef FAT32_H
#define FAT32_H

void fat32_init(void);
int fat32_read(const char *path, void *buf, unsigned long len);
int fat32_write(const char *path, const void *buf, unsigned long len);

#endif // FAT32_H

#ifndef FAT32_H
#define FAT32_H

void fat32_init(void);
void fat32_format(void);
void fat32_list(void (*cb)(const char *name));
int fat32_read(const char *path, void *buf, unsigned long len);
int fat32_write(const char *path, const void *buf, unsigned long len);

#endif // FAT32_H

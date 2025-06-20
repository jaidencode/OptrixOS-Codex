#ifndef EXT2_H
#define EXT2_H

void ext2_init(void);
void ext2_format(void);
void ext2_list(void (*cb)(const char *name));
int ext2_read(const char *path, void *buf, unsigned long len);
int ext2_write(const char *path, const void *buf, unsigned long len);

#endif // EXT2_H

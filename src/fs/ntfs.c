#include "ntfs.h"
#include "../string.h"

typedef struct {
    const char *name;
    char data[512];
    unsigned long size;
} ntfs_file_t;

static ntfs_file_t files[4];
static unsigned long file_count = 0;

static ntfs_file_t *find(const char *path) {
    for (unsigned long i = 0; i < file_count; i++) {
        if (strcmp(files[i].name, path) == 0)
            return &files[i];
    }
    return NULL;
}

void ntfs_init(void) {
    file_count = 1;
    files[0].name = "ntfsfile.txt";
    const char *msg = "Hello from NTFS";
    files[0].size = strlen(msg);
    memcpy(files[0].data, msg, files[0].size);
}

int ntfs_read(const char *path, void *buf, unsigned long len) {
    ntfs_file_t *f = find(path);
    if (!f)
        return -1;
    if (len > f->size)
        len = f->size;
    memcpy(buf, f->data, len);
    return (int)len;
}

int ntfs_write(const char *path, const void *buf, unsigned long len) {
    ntfs_file_t *f = find(path);
    if (!f) {
        if (file_count >= 4)
            return -1;
        f = &files[file_count++];
        f->name = path;
    }
    if (len > sizeof(f->data))
        len = sizeof(f->data);
    memcpy(f->data, buf, len);
    f->size = len;
    return (int)len;
}

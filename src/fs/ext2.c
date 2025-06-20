#include "ext2.h"
#include "../string.h"

typedef struct {
    const char *name;
    char data[512];
    unsigned long size;
} ext2_file_t;

static ext2_file_t files[4];
static unsigned long file_count = 0;

static ext2_file_t *find(const char *path) {
    for (unsigned long i = 0; i < file_count; i++) {
        if (strcmp(files[i].name, path) == 0)
            return &files[i];
    }
    return NULL;
}

void ext2_init(void) {
    file_count = 1;
    files[0].name = "hello.txt";
    const char *msg = "Hello from ext2";
    files[0].size = strlen(msg);
    memcpy(files[0].data, msg, files[0].size);
}

int ext2_read(const char *path, void *buf, unsigned long len) {
    ext2_file_t *f = find(path);
    if (!f)
        return -1;
    if (len > f->size)
        len = f->size;
    memcpy(buf, f->data, len);
    return (int)len;
}

int ext2_write(const char *path, const void *buf, unsigned long len) {
    ext2_file_t *f = find(path);
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

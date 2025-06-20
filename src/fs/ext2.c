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

static char names[4][32];

void ext2_init(void) {
    ext2_format();
}

void ext2_load(const void *data, unsigned long size) {
    const unsigned char *p = (const unsigned char *)data;
    const unsigned char *end = p + size;
    if (size < 4)
        return;

    unsigned long count;
    memcpy(&count, p, 4);
    p += 4;
    file_count = 0;
    for (unsigned long i = 0; i < count && p < end && file_count < 4; i++) {
        unsigned long nlen;
        if (p + 4 > end)
            break;
        memcpy(&nlen, p, 4);
        p += 4;
        if (nlen >= sizeof(names[0]) || p + nlen > end)
            break;
        memcpy(names[file_count], p, nlen);
        names[file_count][nlen] = 0;
        p += nlen;
        unsigned long fsize;
        if (p + 4 > end)
            break;
        memcpy(&fsize, p, 4);
        p += 4;
        if (p + fsize > end)
            break;
        if (fsize > sizeof(files[file_count].data))
            fsize = sizeof(files[file_count].data);
        memcpy(files[file_count].data, p, fsize);
        files[file_count].size = fsize;
        files[file_count].name = names[file_count];
        p += fsize;
        file_count++;
    }
}

void ext2_format(void) {
    file_count = 0;
}

void ext2_list(void (*cb)(const char *name)) {
    for (unsigned long i = 0; i < file_count; i++)
        cb(files[i].name);
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

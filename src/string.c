#include "string.h"

size_t strlen(const char *s) {
    size_t i = 0;
    while (s[i])
        i++;
    return i;
}

void *memcpy(void *dest, const void *src, size_t n) {
    unsigned char *d = dest;
    const unsigned char *s = src;
    for (size_t i = 0; i < n; i++)
        d[i] = s[i];
    return dest;
}

void *memset(void *dest, int c, size_t n) {
    unsigned char *d = dest;
    for (size_t i = 0; i < n; i++)
        d[i] = (unsigned char)c;
    return dest;
}

int strcmp(const char *a, const char *b) {
    while (*a && (*a == *b)) {
        a++;
        b++;
    }
    return *(const unsigned char *)a - *(const unsigned char *)b;
}

int strncmp(const char *a, const char *b, size_t n) {
    for (size_t i = 0; i < n; i++) {
        if (a[i] != b[i] || !a[i] || !b[i])
            return (unsigned char)a[i] - (unsigned char)b[i];
    }
    return 0;
}

char *strchr(const char *s, int c) {
    while (*s) {
        if (*s == c)
            return (char *)s;
        s++;
    }
    return NULL;
}

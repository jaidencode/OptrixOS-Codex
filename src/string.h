#ifndef STRING_H
#define STRING_H
#include <stddef.h>
size_t strlen(const char *s);
void *memcpy(void *dest, const void *src, size_t n);
void *memset(void *dest, int c, size_t n);
int strcmp(const char *a, const char *b);
int strncmp(const char *a, const char *b, size_t n);
#endif

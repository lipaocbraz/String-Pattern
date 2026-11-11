#ifndef SEARCH_H
#define SEARCH_H

#include <stddef.h>

typedef struct {
    size_t count;
    unsigned long checksum;
} Result;

Result naive_search(const char *T, size_t n, const char *P, size_t m);
Result kmp_search(const char *T, size_t n, const char *P, size_t m);

#endif

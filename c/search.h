#ifndef SEARCH_H
#define SEARCH_H

#include <stddef.h>
#include <stdint.h>

/* count = nº de ocorrências (com sobreposição);
 * checksum = soma das posições (0-based) das ocorrências, mod 2^32.
 * m == 0 ou m > n => count 0. */
typedef struct {
    size_t count;
    uint32_t checksum;
} Result;

Result naive_search(const char *T, size_t n, const char *P, size_t m);
Result kmp_search(const char *T, size_t n, const char *P, size_t m);

#endif

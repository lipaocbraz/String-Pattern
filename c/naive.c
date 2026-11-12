#include "search.h"

Result naive_search(const char *T, size_t n, const char *P, size_t m) {
    Result r = {0, 0};
    if (m == 0 || m > n) return r;
    for (size_t i = 0; i + m <= n; i++) {
        size_t j = 0;
        while (j < m && T[i + j] == P[j]) j++;
        if (j == m) {
            r.count++;
            r.checksum += (uint32_t)i;
        }
    }
    return r;
}

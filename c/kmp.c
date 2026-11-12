#include <stdlib.h>

#include "search.h"

Result kmp_search(const char *T, size_t n, const char *P, size_t m) {
    Result r = {0, 0};
    if (m == 0 || m > n) return r;

    size_t *fail = malloc(m * sizeof *fail);
    if (!fail) abort();

    fail[0] = 0;
    for (size_t i = 1, k = 0; i < m; i++) {
        while (k > 0 && P[i] != P[k]) k = fail[k - 1];
        if (P[i] == P[k]) k++;
        fail[i] = k;
    }

    for (size_t i = 0, k = 0; i < n; i++) {
        while (k > 0 && T[i] != P[k]) k = fail[k - 1];
        if (T[i] == P[k]) k++;
        if (k == m) {
            r.count++;
            r.checksum += (uint32_t)(i + 1 - m);
            k = fail[k - 1];
        }
    }

    free(fail);
    return r;
}

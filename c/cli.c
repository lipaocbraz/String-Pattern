/* Uso: cli <naive|kmp> T.txt P.txt  ->  imprime "count checksum" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "io.h"
#include "search.h"

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "uso: %s <naive|kmp> T.txt P.txt\n", argv[0]);
        return 2;
    }
    size_t n, m;
    char *T = read_file(argv[2], &n);
    char *P = read_file(argv[3], &m);
    if (!T || !P) {
        fprintf(stderr, "erro ao ler entrada\n");
        return 1;
    }

    Result r;
    if (strcmp(argv[1], "naive") == 0) r = naive_search(T, n, P, m);
    else if (strcmp(argv[1], "kmp") == 0) r = kmp_search(T, n, P, m);
    else {
        fprintf(stderr, "algoritmo desconhecido: %s\n", argv[1]);
        return 2;
    }

    printf("%zu %u\n", r.count, r.checksum);
    free(T);
    free(P);
    return 0;
}

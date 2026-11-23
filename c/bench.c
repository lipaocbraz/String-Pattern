/* Uso: bench [data_dir]  ->  CSV em stdout */
#define _POSIX_C_SOURCE 200809L

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <time.h>
#endif

#include "io.h"
#include "search.h"

typedef Result (*SearchFn)(const char *, size_t, const char *, size_t);

enum { REPETITIONS = 20, WARMUP = 3 };

#ifdef _WIN32
static LARGE_INTEGER ticks_per_second;
#endif

static double now(void) {
#ifdef _WIN32
    LARGE_INTEGER ticks;
    QueryPerformanceCounter(&ticks);
    return (double)ticks.QuadPart / ticks_per_second.QuadPart;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
#endif
}

static int run_case(const char *root, const char *dir) {
    char path[1536], exp[16], type[16];
    if (sscanf(dir, "%15[^/]/%15[^/]", exp, type) != 2) {
        fprintf(stderr, "caso inválido: %s\n", dir);
        return 0;
    }

    size_t n, m;
    snprintf(path, sizeof path, "%s/%s/T.txt", root, dir);
    char *T = read_file(path, &n);
    snprintf(path, sizeof path, "%s/%s/P.txt", root, dir);
    char *P = read_file(path, &m);
    if (!T || !P) {
        fprintf(stderr, "erro ao ler %s\n", dir);
        free(T);
        free(P);
        return 0;
    }

    const char *names[] = {"naive", "kmp"};
    SearchFn fns[] = {naive_search, kmp_search};
    for (int a = 0; a < 2; a++) {
        for (int j = 0; j < WARMUP; j++) {
            fns[a](T, n, P, m);
        }

        Result r = {0, 0};
        double mean = 0, sum_squares = 0;
        for (int j = 1; j <= REPETITIONS; j++) {
            double start = now();
            r = fns[a](T, n, P, m);
            double elapsed = now() - start;
            double delta = elapsed - mean;
            mean += delta / j;
            sum_squares += delta * (elapsed - mean);
        }
        double deviation = sqrt(sum_squares / (REPETITIONS - 1));
        printf("%s,%s,%zu,%zu,%s,%.12f,%zu,%u,%.12f,%d\n",
               exp, type, n, m, names[a], mean, r.count, r.checksum, deviation, REPETITIONS);
    }
    free(T);
    free(P);
    return 1;
}

int main(int argc, char **argv) {
    const char *root = argc > 1 ? argv[1] : "data";
    char path[1024];
    if (snprintf(path, sizeof path, "%s/cases.txt", root) >= (int)sizeof path) {
        fprintf(stderr, "caminho de dados longo demais\n");
        return 1;
    }
    FILE *cases = fopen(path, "r");
    if (!cases) {
        fprintf(stderr, "erro ao abrir %s; rode make data\n", path);
        return 1;
    }
#ifdef _WIN32
    if (!QueryPerformanceFrequency(&ticks_per_second)) {
        fprintf(stderr, "relógio de alta resolução indisponível\n");
        fclose(cases);
        return 1;
    }
#endif

    puts("exp,type,n,m,algo,time_s,count,checksum,stddev_s,repetitions");
    char dir[256];
    size_t count = 0;
    while (fscanf(cases, "%255s", dir) == 1) {
        if (!run_case(root, dir)) {
            fclose(cases);
            return 1;
        }
        count++;
    }
    int failed = ferror(cases);
    fclose(cases);
    if (failed || count == 0) {
        fprintf(stderr, "erro ao ler os casos em %s\n", path);
        return 1;
    }
    return fflush(stdout) == EOF;
}

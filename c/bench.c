/* Uso: bench [data_dir]  ->  CSV em stdout
 * Percorre exp1 (random, worst, best) e exp2 (worst) sob data_dir.
 * Cada medida é a média de várias repetições (>= 0.2 s no total ou 1000 reps). */
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "io.h"
#include "search.h"

typedef Result (*SearchFn)(const char *, size_t, const char *, size_t);

static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static void run_case(const char *exp, const char *type, const char *dir) {
    char path[1024];
    size_t n, m;
    snprintf(path, sizeof path, "%s/T.txt", dir);
    char *T = read_file(path, &n);
    snprintf(path, sizeof path, "%s/P.txt", dir);
    char *P = read_file(path, &m);
    if (!T || !P) {
        fprintf(stderr, "pulando %s\n", dir);
        free(T);
        free(P);
        return;
    }

    const char *names[] = {"naive", "kmp"};
    SearchFn fns[] = {naive_search, kmp_search};
    for (int a = 0; a < 2; a++) {
        Result r = fns[a](T, n, P, m); /* aquecimento + resultado */
        int reps = 0;
        double t0 = now(), elapsed;
        do {
            r = fns[a](T, n, P, m);
            reps++;
            elapsed = now() - t0;
        } while (elapsed < 0.2 && reps < 1000);
        printf("%s,%s,%zu,%zu,%s,%.9f,%zu,%u\n", exp, type, n, m, names[a],
               elapsed / reps, r.count, r.checksum);
        fflush(stdout);
    }
    free(T);
    free(P);
}

static void run_group(const char *root, const char *exp, const char *type) {
    char base[1024];
    snprintf(base, sizeof base, "%s/%s/%s", root, exp, type);
    DIR *d = opendir(base);
    if (!d) return;
    struct dirent *e;
    while ((e = readdir(d))) {
        if (e->d_name[0] != 'n') continue;
        char dir[1536];
        snprintf(dir, sizeof dir, "%s/%s", base, e->d_name);
        run_case(exp, type, dir);
    }
    closedir(d);
}

int main(int argc, char **argv) {
    const char *root = argc > 1 ? argv[1] : "data";
    printf("exp,type,n,m,algo,time_s,count,checksum\n");
    run_group(root, "exp1", "random");
    run_group(root, "exp1", "worst");
    run_group(root, "exp1", "best");
    run_group(root, "exp2", "worst");
    return 0;
}

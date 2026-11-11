#ifndef IO_H
#define IO_H

#include <stddef.h>

/* Lê o arquivo inteiro; retorna buffer alocado (free pelo chamador). */
char *read_file(const char *path, size_t *len);

#endif

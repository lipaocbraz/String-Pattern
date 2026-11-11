CC     = gcc
CFLAGS = -O2 -Wall -Wextra
SRC    = naive.c kmp.c io.c

all: bin/bench bin/cli

bin:
	mkdir -p bin

bin/bench: bench.c $(SRC) search.h io.h | bin
	$(CC) $(CFLAGS) -o $@ bench.c $(SRC)

bin/cli: cli.c $(SRC) search.h io.h | bin
	$(CC) $(CFLAGS) -o $@ cli.c $(SRC)

clean:
	rm -rf bin

.PHONY: all clean

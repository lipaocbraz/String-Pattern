CC     = gcc
CFLAGS = -O2 -Wall -Wextra
LDLIBS = -lm
SRC    = naive.c kmp.c io.c

ifeq ($(OS),Windows_NT)
EXEEXT := .exe
endif

all: bin/bench$(EXEEXT) bin/cli$(EXEEXT)

bin:
	mkdir -p bin

bin/bench$(EXEEXT): bench.c $(SRC) search.h io.h | bin
	$(CC) $(CFLAGS) -o $@ bench.c $(SRC) $(LDLIBS)

bin/cli$(EXEEXT): cli.c $(SRC) search.h io.h | bin
	$(CC) $(CFLAGS) -o $@ cli.c $(SRC)

clean:
	rm -rf bin

.PHONY: all clean

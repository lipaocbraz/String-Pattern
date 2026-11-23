.PHONY: data build test bench plots all

PYTHON ?= python3
ifeq ($(OS),Windows_NT)
EXEEXT := .exe
endif

data:
	$(PYTHON) gen/generate.py

build:
	$(MAKE) -C c

test: build data
	$(PYTHON) -m unittest discover -s tests -v

bench: build data
	./c/bin/bench$(EXEEXT) > results/c.csv.tmp && $(PYTHON) python/bench.py > results/python.csv.tmp
	mv results/c.csv.tmp results/c.csv
	mv results/python.csv.tmp results/python.csv

plots:
	$(PYTHON) plots/make_plots.py

all: test bench
	$(MAKE) plots

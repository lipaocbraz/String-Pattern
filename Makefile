.PHONY: data build test bench plots all

data:
	python3 gen/generate.py

build:
	$(MAKE) -C c

test: build data
	python3 -m pytest tests

bench: build data
	./c/bin/bench > results/c.csv
	python3 python/bench.py > results/python.csv

plots:
	python3 plots/make_plots.py

all: data build test bench plots

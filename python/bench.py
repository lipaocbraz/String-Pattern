"""Uso: python3 python/bench.py [data_dir]  ->  CSV em stdout (mesmo formato do bench C)."""
import sys
import time
from pathlib import Path
from statistics import mean, stdev

from io_utils import read_case
from kmp import kmp_search
from naive import naive_search

ALGOS = {"naive": naive_search, "kmp": kmp_search}
REPETITIONS = 20
WARMUP = 3


def measure(fn, t, p):
    for _ in range(WARMUP):
        fn(t, p)

    samples = []
    for _ in range(REPETITIONS):
        start = time.perf_counter_ns()
        res = fn(t, p)
        elapsed = time.perf_counter_ns() - start
        samples.append(elapsed)
    return mean(samples) * 1e-9, stdev(samples) * 1e-9, res


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "data")
    cases = (root / "cases.txt").read_text(encoding="ascii").splitlines()
    if not cases:
        raise SystemExit("Lista de casos vazia. Rode make data.")

    print("exp,type,n,m,algo,time_s,count,checksum,stddev_s,repetitions")
    for case in cases:
        exp, kind, _ = case.split("/")
        t, p = read_case(root / case)
        for name, fn in ALGOS.items():
            secs, deviation, (count, checksum) = measure(fn, t, p)
            print(
                f"{exp},{kind},{len(t)},{len(p)},{name},{secs:.12f},{count},{checksum},"
                f"{deviation:.12f},{REPETITIONS}",
                flush=True,
            )


if __name__ == "__main__":
    main()

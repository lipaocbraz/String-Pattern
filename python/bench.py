"""Uso: python3 python/bench.py [data_dir]  ->  CSV em stdout (mesmo formato do bench C)."""
import sys
import time
from pathlib import Path

from io_utils import read_case
from kmp import kmp_search
from naive import naive_search

ALGOS = {"naive": naive_search, "kmp": kmp_search}
GROUPS = [("exp1", "random"), ("exp1", "worst"), ("exp1", "best"), ("exp2", "worst")]


def measure(fn, t, p):
    res = fn(t, p)  # aquecimento + resultado
    reps, t0 = 0, time.perf_counter()
    while True:
        res = fn(t, p)
        reps += 1
        elapsed = time.perf_counter() - t0
        if elapsed >= 0.2 or reps >= 1000:
            return elapsed / reps, res


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "data")
    print("exp,type,n,m,algo,time_s,count,checksum")
    for exp, typ in GROUPS:
        base = root / exp / typ
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            t, p = read_case(d)
            for name, fn in ALGOS.items():
                secs, (count, checksum) = measure(fn, t, p)
                print(f"{exp},{typ},{len(t)},{len(p)},{name},{secs:.9f},{count},{checksum}",
                      flush=True)


if __name__ == "__main__":
    main()

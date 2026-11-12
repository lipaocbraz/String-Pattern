"""Gera todas as entradas em data/ (seed 42).

Layout: data/<exp>/<tipo>/n<N>_m<M>/{T.txt,P.txt}
  exp1: varia n (m fixo)      tipos: random, worst, best
  exp2: varia m (n fixo)      tipo:  worst
  edge: casos de borda        data/edge/<nome>/{T.txt,P.txt}
"""
import random
from pathlib import Path

SEED = 42
ROOT = Path(__file__).resolve().parent.parent / "data"
ALPHABET = "ACGT"

EXP1_N = [1_000, 10_000, 100_000, 1_000_000]
EXP1_M = 100
EXP2_N = 100_000
EXP2_M = [10, 50, 100, 500, 1_000]

EDGE = {
    "single_match": ("abcde", "cde"),
    "overlap": ("aaaaa", "aa"),
    "m_eq_n_match": ("abc", "abc"),
    "m_eq_n_nomatch": ("abc", "abd"),
    "m_gt_n": ("ab", "abc"),
    "no_match": ("abcdefgh", "xyz"),
    "single_char": ("abab", "a"),
    "periodic": ("abababab", "abab"),
    "match_at_end": ("xxxxabc", "abc"),
}


def write(d: Path, t: str, p: str) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "T.txt").write_text(t)
    (d / "P.txt").write_text(p)


def random_case(rng: random.Random, n: int, m: int) -> tuple[str, str]:
    t = "".join(rng.choices(ALPHABET, k=n))
    start = rng.randrange(n - m + 1)  # P sai de T: garante >= 1 ocorrência
    return t, t[start:start + m]


def worst_case(n: int, m: int) -> tuple[str, str]:
    return "a" * n, "a" * (m - 1) + "b"  # naive faz ~(n-m+1)*m comparações


def best_case(n: int, m: int) -> tuple[str, str]:
    return "a" * n, "b" * m  # naive falha na 1ª comparação de cada posição


def main() -> None:
    rng = random.Random(SEED)
    for n in EXP1_N:
        name = f"n{n}_m{EXP1_M}"
        write(ROOT / "exp1" / "random" / name, *random_case(rng, n, EXP1_M))
        write(ROOT / "exp1" / "worst" / name, *worst_case(n, EXP1_M))
        write(ROOT / "exp1" / "best" / name, *best_case(n, EXP1_M))
    for m in EXP2_M:
        write(ROOT / "exp2" / "worst" / f"n{EXP2_N}_m{m}", *worst_case(EXP2_N, m))
    for name, (t, p) in EDGE.items():
        write(ROOT / "edge" / name, t, p)
    print(f"dados gerados em {ROOT}")


if __name__ == "__main__":
    main()

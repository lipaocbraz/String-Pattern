"""Gera todas as entradas em data/ (seed 42).

Layout: data/<exp>/<tipo>/n<N>_m<M>/{T.txt,P.txt}
  exp1: varia n (m fixo)      tipos: random, worst, best
  exp2: varia m (n fixo)      tipo:  worst
  edge: casos de borda        data/edge/<nome>/{T.txt,P.txt}
  cases.txt: caminhos relativos dos casos medidos, em ordem de geração
"""
import random
from pathlib import Path

SEED = 42
ROOT = Path(__file__).resolve().parent.parent / "data"
ALPHABET = "ACGT"

EXP1_N = [4_000, 8_000, 16_000, 32_000, 64_000, 128_000]
EXP1_M = 100
EXP2_N = 128_000
EXP2_M = [8, 16, 32, 64, 128, 256]

EDGE = {
    "single_match": ("abcde", "cde"),
    "overlap": ("aaaaa", "aa"),
    "m_eq_n_match": ("abc", "abc"),
    "m_eq_n_nomatch": ("abc", "abd"),
    "m_gt_n": ("ab", "abc"),
    "no_match": ("abcdefgh", "xyz"),
    "single_char": ("abab", "a"),
    "empty_pattern": ("abc", ""),
    "empty_text": ("", "abc"),
    "periodic": ("abababab", "abab"),
    "match_at_end": ("xxxxabc", "abc"),
}


def write(d: Path, t: str, p: str) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "T.txt").write_text(t, encoding="ascii")
    (d / "P.txt").write_text(p, encoding="ascii")


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
    cases = []
    for n in EXP1_N:
        inputs = {
            "random": random_case(rng, n, EXP1_M),
            "worst": worst_case(n, EXP1_M),
            "best": best_case(n, EXP1_M),
        }
        for kind, (t, p) in inputs.items():
            case = Path("exp1", kind, f"n{n}_m{EXP1_M}")
            write(ROOT / case, t, p)
            cases.append(case.as_posix())
    for m in EXP2_M:
        case = Path("exp2", "worst", f"n{EXP2_N}_m{m}")
        write(ROOT / case, *worst_case(EXP2_N, m))
        cases.append(case.as_posix())
    (ROOT / "cases.txt").write_text("\n".join(cases) + "\n", encoding="ascii")
    for name, (t, p) in EDGE.items():
        write(ROOT / "edge" / name, t, p)
    print(f"dados gerados em {ROOT}")


if __name__ == "__main__":
    main()

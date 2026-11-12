"""Compara as 4 implementações (C naive/kmp via cli, Python naive/kmp)
entre si e contra um oráculo independente (str.find)."""
import random
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from io_utils import read_case  # noqa: E402
from kmp import kmp_search  # noqa: E402
from naive import naive_search  # noqa: E402

CLI = ROOT / "c" / "bin" / "cli"


def oracle(t: str, p: str) -> tuple[int, int]:
    if not p or len(p) > len(t):
        return 0, 0
    count = checksum = 0
    i = t.find(p)
    while i != -1:
        count += 1
        checksum += i
        i = t.find(p, i + 1)
    return count, checksum & 0xFFFFFFFF


def c_search(algo: str, d: Path) -> tuple[int, int]:
    out = subprocess.run([str(CLI), algo, str(d / "T.txt"), str(d / "P.txt")],
                         capture_output=True, text=True, check=True).stdout
    count, checksum = out.split()
    return int(count), int(checksum)


def check_dir(d: Path) -> None:
    t, p = read_case(d)
    expected = oracle(t, p)
    assert naive_search(t, p) == expected
    assert kmp_search(t, p) == expected
    assert c_search("naive", d) == expected
    assert c_search("kmp", d) == expected


EDGE_DIRS = sorted((ROOT / "data" / "edge").glob("*")) if (ROOT / "data" / "edge").is_dir() else []


def test_edge_data_present():
    assert EDGE_DIRS, "rode `make data` antes dos testes"


@pytest.mark.parametrize("d", EDGE_DIRS, ids=lambda d: d.name)
def test_edge(d):
    check_dir(d)


@pytest.mark.parametrize("seed", range(30))
def test_random_small(tmp_path, seed):
    rng = random.Random(seed)
    alphabet = rng.choice(["ab", "abc", "ACGT"])
    t = "".join(rng.choices(alphabet, k=rng.randint(1, 200)))
    p = "".join(rng.choices(alphabet, k=rng.randint(1, 6)))
    (tmp_path / "T.txt").write_text(t)
    (tmp_path / "P.txt").write_text(p)
    check_dir(tmp_path)


@pytest.mark.parametrize("d", sorted((ROOT / "data" / "exp1").glob("*/n1000_*")), ids=lambda d: d.parent.name)
def test_exp1_smallest(d):
    check_dir(d)

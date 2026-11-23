"""Compara as 4 implementações (C naive/kmp via cli, Python naive/kmp)
entre si e contra um oráculo independente (str.find)."""
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from io_utils import read_case  # noqa: E402
from kmp import kmp_search  # noqa: E402
from naive import naive_search  # noqa: E402

CLI = ROOT / "c" / "bin" / ("cli.exe" if sys.platform == "win32" else "cli")
DATA = ROOT / "data"


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


CASE_TYPES = ("random", "worst", "best")


class SearchCorrectness(unittest.TestCase):
    def test_edge(self):
        cases = sorted((DATA / "edge").glob("*"))
        self.assertTrue(cases, "rode `make data` antes dos testes")
        for case in cases:
            with self.subTest(case=case.name):
                check_dir(case)

    def test_random_small(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for seed in range(30):
                with self.subTest(seed=seed):
                    rng = random.Random(seed)
                    alphabet = rng.choice(["ab", "abc", "ACGT"])
                    t = "".join(rng.choices(alphabet, k=rng.randint(1, 200)))
                    p = "".join(rng.choices(alphabet, k=rng.randint(1, 6)))
                    (path / "T.txt").write_text(t, encoding="ascii")
                    (path / "P.txt").write_text(p, encoding="ascii")
                    check_dir(path)

    def test_exp1_smallest(self):
        cases = (DATA / "cases.txt").read_text(encoding="ascii").splitlines()
        for kind in CASE_TYPES:
            with self.subTest(kind=kind):
                group = [case for case in cases if case.startswith(f"exp1/{kind}/")]
                self.assertTrue(group, "rode `make data` antes dos testes")
                check_dir(DATA / group[0])

from pathlib import Path


def read_case(d) -> tuple[str, str]:
    """Lê T.txt e P.txt de um diretório de caso."""
    d = Path(d)
    t = (d / "T.txt").read_text().rstrip("\r\n")
    p = (d / "P.txt").read_text().rstrip("\r\n")
    return t, p

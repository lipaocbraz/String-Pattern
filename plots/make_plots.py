"""Lê results/{c,python}.csv e gera os PNGs em plots/output/."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "plots" / "output"
CASE = ["exp", "type", "n", "m"]
LABELS = {"random": "Aleatório", "worst": "Pior caso da busca ingênua",
          "best": "Melhor caso da busca ingênua"}
STYLES = {
    "C / ingênua": ("#17668e", "o"),
    "C / KMP": ("#087a66", "s"),
    "Python / ingênua": ("#b34a25", "o"),
    "Python / KMP": ("#754393", "s"),
}


def load() -> pd.DataFrame:
    frames = []
    for filename, lang in (("c.csv", "C"), ("python.csv", "Python")):
        df = pd.read_csv(ROOT / "results" / filename)
        df["lang"] = lang
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["impl"] = df["lang"] + " / " + df["algo"].map({"naive": "ingênua", "kmp": "KMP"})
    metrics = df[["time_s", "stddev_s", "repetitions"]]
    if (df["impl"].isna().any() or metrics.isna().any().any()
            or not df["repetitions"].between(15, 30).all()
            or (df["time_s"] <= 0).any() or (df["stddev_s"] < 0).any()):
        raise ValueError("Resultados inválidos. Execute os dois benchmarks novamente.")
    grouped = df.groupby(CASE)
    if (not grouped.size().eq(4).all()
            or not grouped[["impl", "count", "checksum"]].nunique().eq([4, 1, 1]).all().all()):
        raise ValueError("As quatro implementações devem concordar em todos os casos.")
    return df


def plot_series(ax, data: pd.DataFrame, size: str, *, ratio: bool = False) -> None:
    for impl, group in data.groupby("impl"):
        group = group.sort_values(size)
        color, marker = STYLES[impl]
        values = group["time_s"]
        if ratio:
            n, m = group["n"], group["m"]
            factor = n + m if group["algo"].iat[0] == "kmp" else n - m + 1
            if group["algo"].iat[0] == "naive" and group["type"].iat[0] == "worst":
                factor = factor * m
            values = values / factor
            values = values / values.iat[0]
        ax.plot(group[size], values, color=color, marker=marker, label=impl)
    ax.set(xscale="log", xlabel=size)
    ax.grid(True, which="both", alpha=0.25)


def plot_exp1(df: pd.DataFrame) -> None:
    sub = df[df["exp"] == "exp1"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2), sharey=True)
    for ax, (kind, label) in zip(axes, LABELS.items()):
        plot_series(ax, sub[sub["type"] == kind], "n")
        ax.set(title=label, yscale="log")
    axes[0].set_ylabel("Tempo médio (s)")
    axes[0].legend()
    fig.suptitle(f"Experimento 1 · comprimento do padrão fixo em {sub['m'].iat[0]}")
    fig.tight_layout()
    fig.savefig(OUT / "exp1_varia_n.png", dpi=180)
    plt.close(fig)


def plot_exp2(df: pd.DataFrame) -> None:
    sub = df[df["exp"] == "exp2"]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    plot_series(ax, sub, "m")
    ax.set(title=f"Experimento 2 · pior caso da busca ingênua, n = {sub['n'].iat[0]}",
           ylabel="Tempo médio (s)", yscale="log")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "exp2_varia_m.png", dpi=180)
    plt.close(fig)


def plot_theory(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), sharey=True)
    for ax, (exp, kind) in zip(axes.flat, [("exp1", kind) for kind in LABELS] + [("exp2", "worst")]):
        size = "n" if exp == "exp1" else "m"
        plot_series(ax, df[(df["exp"] == exp) & (df["type"] == kind)], size, ratio=True)
        ax.axhline(1, color="0.5", linestyle="--", linewidth=0.9)
        ax.set_title(f"{LABELS[kind]} · varia {size}")
    axes[0, 0].set_ylabel("Razão relativa")
    axes[1, 0].set_ylabel("Razão relativa")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4)
    fig.suptitle("Tempo médio / custo teórico, normalizado pelo primeiro ponto")
    fig.tight_layout(rect=(0, 0.065, 1, 1))
    fig.savefig(OUT / "teoria_medido.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load()
    plot_exp1(df)
    plot_exp2(df)
    plot_theory(df)
    print(f"PNGs em {OUT}")


if __name__ == "__main__":
    main()

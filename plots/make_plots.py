"""Lê results/{c,python}.csv e gera os PNGs em plots/output/."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "plots" / "output"


def load() -> pd.DataFrame:
    frames = []
    for lang in ("c", "python"):
        df = pd.read_csv(ROOT / "results" / f"{lang}.csv")
        df["lang"] = lang
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["impl"] = df["lang"] + "-" + df["algo"]
    return df


def plot_exp1(df: pd.DataFrame) -> None:
    sub = df[df["exp"] == "exp1"]
    types = ["random", "worst", "best"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    for ax, typ in zip(axes, types):
        for impl, g in sub[sub["type"] == typ].groupby("impl"):
            g = g.sort_values("n")
            ax.plot(g["n"], g["time_s"], marker="o", label=impl)
        ax.set(title=f"exp1 ({typ}, m fixo)", xlabel="n", xscale="log", yscale="log")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("tempo (s)")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(OUT / "exp1_varia_n.png", dpi=150)
    plt.close(fig)


def plot_exp2(df: pd.DataFrame) -> None:
    sub = df[df["exp"] == "exp2"]
    fig, ax = plt.subplots(figsize=(6, 4))
    for impl, g in sub.groupby("impl"):
        g = g.sort_values("m")
        ax.plot(g["m"], g["time_s"], marker="o", label=impl)
    ax.set(title="exp2 (pior caso, n fixo)", xlabel="m", ylabel="tempo (s)",
           xscale="log", yscale="log")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "exp2_varia_m.png", dpi=150)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load()
    plot_exp1(df)
    plot_exp2(df)
    print(f"PNGs em {OUT}")


if __name__ == "__main__":
    main()

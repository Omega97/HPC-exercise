#!/usr/bin/env python3
"""Generate strong/weak scaling plots from ex2 OMP EPYC CSVs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PLOTS = ROOT / "plots"
PLOTS.mkdir(parents=True, exist_ok=True)


def load_csv(name: str) -> pd.DataFrame:
    df = pd.read_csv(RESULTS / name)
    df.columns = ["threads", "size", "walltime"]
    return df


def plot_strong(df: pd.DataFrame) -> None:
    t1 = df.loc[df["threads"] == 1, "walltime"].iloc[0]
    speedup = t1 / df["walltime"]
    efficiency = speedup / df["threads"] * 100

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    axes[0].plot(df["threads"], df["walltime"], "o-", color="#2563eb")
    axes[0].set_xlabel("Threads")
    axes[0].set_ylabel("Walltime (s)")
    axes[0].set_title("Strong scaling — walltime")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(df["threads"], speedup, "o-", color="#16a34a")
    axes[1].plot(df["threads"], df["threads"], "--", color="#9ca3af", label="ideal")
    axes[1].set_xlabel("Threads")
    axes[1].set_ylabel("Speedup")
    axes[1].set_title("Strong scaling — speedup")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(df["threads"], efficiency, "o-", color="#dc2626")
    axes[2].axhline(100, linestyle="--", color="#9ca3af", linewidth=1)
    axes[2].set_xlabel("Threads")
    axes[2].set_ylabel("Efficiency (%)")
    axes[2].set_title("Strong scaling — efficiency")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("OpenMP strong scaling (EPYC, 1000×1000, I_max=65535)", fontsize=12)
    fig.tight_layout()
    fig.savefig(PLOTS / "strong_scaling_OMP_EPYC.png", dpi=150)
    plt.close(fig)


def plot_weak(df: pd.DataFrame) -> None:
    t_ref = df.loc[df["threads"] == 1, "walltime"].iloc[0]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].plot(df["threads"], df["walltime"], "o-", color="#2563eb", label="measured")
    axes[0].axhline(t_ref, linestyle="--", color="#9ca3af", label=f"ideal (T₁={t_ref:.1f} s)")
    axes[0].set_xlabel("Threads")
    axes[0].set_ylabel("Walltime (s)")
    axes[0].set_title("Weak scaling — walltime")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(df["threads"], df["size"], "o-", color="#7c3aed")
    axes[1].set_xlabel("Threads")
    axes[1].set_ylabel("Image size (pixels)")
    axes[1].set_title("Weak scaling — problem size")
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("OpenMP weak scaling (EPYC, C=1e6 px/thread)", fontsize=12)
    fig.tight_layout()
    fig.savefig(PLOTS / "weak_scaling_OMP_EPYC.png", dpi=150)
    plt.close(fig)


def main() -> None:
    strong = load_csv("strong_scaling_OMP_EPYC.csv")
    weak = load_csv("weak_scaling_OMP_EPYC.csv")
    plot_strong(strong)
    plot_weak(weak)
    print(f"Wrote {PLOTS / 'strong_scaling_OMP_EPYC.png'}")
    print(f"Wrote {PLOTS / 'weak_scaling_OMP_EPYC.png'}")


if __name__ == "__main__":
    main()
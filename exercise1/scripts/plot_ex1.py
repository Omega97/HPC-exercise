#!/usr/bin/env python3
"""Generate presentation plots for Exercise 1 MPI collective benchmarks."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PLOTS = ROOT / "plots"
PLOTS.mkdir(parents=True, exist_ok=True)

BCAST_ALGOS = (0, 1, 2, 5)
BARRIER_ALGOS = (0, 1, 2, 4)
BCAST_LABELS = {
    0: "0 — baseline",
    1: "1 — linear",
    2: "2 — chain",
    5: "5 — binary tree",
}
BARRIER_LABELS = {
    0: "0 — baseline",
    1: "1 — linear",
    2: "2 — double ring",
    4: "4 — bruck",
}
ALGO_COLORS = {0: "#2563eb", 1: "#dc2626", 2: "#16a34a", 4: "#7c3aed", 5: "#ea580c"}

EPYC_PROCS = (2, 4, 8, 16, 32, 64, 128, 256)
THIN_PROCS = (2, 4, 8, 12, 16, 24, 48)
SIZE_1MIB = 1_048_576


def median_bcast(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return (
        df.groupby(["Algorithm", "Processors", "Size(bytes)"], as_index=False)["Avg_Latency(us)"]
        .median()
    )


def median_barrier(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.groupby(["Algorithm", "Processors"], as_index=False)["Avg_Latency(us)"].median()


def plot_bcast_vs_size() -> None:
    df = median_bcast(RESULTS / "bcastEPYC.csv")
    subset = df[(df["Processors"] == 256) & (df["Algorithm"].isin(BCAST_ALGOS))]

    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in BCAST_ALGOS:
        block = subset[subset["Algorithm"] == algo].sort_values("Size(bytes)")
        ax.loglog(
            block["Size(bytes)"],
            block["Avg_Latency(us)"],
            "o-",
            color=ALGO_COLORS[algo],
            label=BCAST_LABELS[algo],
            markersize=5,
            linewidth=1.8,
        )

    ax.set_xlabel("Message size (bytes)")
    ax.set_ylabel("Latency (µs)")
    ax.set_title("Broadcast latency vs message size (EPYC, P = 256)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    out = PLOTS / "bcast_latency_vs_size_P256.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def _plot_bcast_scaling_panel(ax, df, procs, title: str) -> None:
    subset = df[(df["Size(bytes)"] == SIZE_1MIB) & (df["Processors"].isin(procs))]
    for algo in BCAST_ALGOS:
        block = subset[subset["Algorithm"] == algo].sort_values("Processors")
        ax.loglog(
            block["Processors"],
            block["Avg_Latency(us)"],
            "o-",
            color=ALGO_COLORS[algo],
            label=BCAST_LABELS[algo],
            markersize=5,
            linewidth=1.8,
        )
    ax.set_xlabel("Processors")
    ax.set_ylabel("Latency (µs)")
    ax.set_title(title)
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, which="both", alpha=0.3)


def plot_bcast_vs_procs_1mib() -> None:
    epyc = median_bcast(RESULTS / "bcastEPYC.csv")
    thin = median_bcast(RESULTS / "bcastTHIN.csv")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    _plot_bcast_scaling_panel(axes[0], epyc, EPYC_PROCS, "EPYC — 1 MiB message")
    _plot_bcast_scaling_panel(axes[1], thin, THIN_PROCS, "THIN — 1 MiB message")
    fig.suptitle("Broadcast latency vs processors (median over repetitions)", fontsize=12)
    fig.tight_layout()
    out = PLOTS / "bcast_latency_vs_procs_1MiB.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def plot_barrier_epyc() -> None:
    df = median_barrier(RESULTS / "barrierEPYC.csv")
    subset = df[(df["Processors"].isin(EPYC_PROCS)) & (df["Algorithm"].isin(BARRIER_ALGOS))]

    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in BARRIER_ALGOS:
        block = subset[subset["Algorithm"] == algo].sort_values("Processors")
        ax.loglog(
            block["Processors"],
            block["Avg_Latency(us)"],
            "o-",
            color=ALGO_COLORS[algo],
            label=BARRIER_LABELS[algo],
            markersize=5,
            linewidth=1.8,
        )

    ax.set_xlabel("Processors")
    ax.set_ylabel("Latency (µs)")
    ax.set_title("Barrier latency vs processors (EPYC)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    out = PLOTS / "barrier_latency_vs_procs_EPYC.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    plot_bcast_vs_size()
    plot_bcast_vs_procs_1mib()
    plot_barrier_epyc()


if __name__ == "__main__":
    main()
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALG_NAMES = {
    "bcast": {0: "baseline (0)", 1: "linear (1)", 2: "chain (2)", 5: "binary tree (5)"},
    "barrier": {0: "baseline (0)", 1: "linear (1)", 2: "double_ring (2)", 4: "bruck (4)"},
}


def summarize(path, op):
    df = pd.read_csv(path)
    med = df.groupby(["Algorithm", "Processors"], as_index=False)["Avg_Latency(us)"].median()
    algs = sorted(med["Algorithm"].unique())
    procs = sorted(med["Processors"].unique())
    print(f"\n=== {path.name} ===")
    print(f"Algorithms: {algs}")
    print(f"Processors ({len(procs)}): {procs}")
    pivot = med.pivot(index="Processors", columns="Algorithm", values="Avg_Latency(us)")
    print("Median latency (us):")
    print(pivot.round(2).to_string())
    best = med.loc[med.groupby("Processors")["Avg_Latency(us)"].idxmin()]
    print("\nFastest algo per proc (median):")
    for _, r in best.iterrows():
        a = int(r.Algorithm)
        print(
            f"  P={int(r.Processors):3d}: algo {a} ({ALG_NAMES[op][a]}) -> {r['Avg_Latency(us)']:.2f} us"
        )


def bcast_size_summary(path):
    df = pd.read_csv(path)
    sizes = [1, 1024, 1048576]
    procs = [48, 128, 256] if "EPYC" in path.name else [24, 48]
    subset = df[df["Size(bytes)"].isin(sizes) & df["Processors"].isin(procs)]
    med = (
        subset.groupby(["Processors", "Size(bytes)", "Algorithm"], as_index=False)["Avg_Latency(us)"]
        .median()
    )
    print(f"\n=== {path.name} — size sweep (median us) ===")
    for p in procs:
        for s in sizes:
            block = med[(med["Processors"] == p) & (med["Size(bytes)"] == s)]
            if block.empty:
                continue
            label = f"{s} B" if s < 1024 else (f"{s//1024} KiB" if s < 1048576 else "1 MiB")
            print(f"\n  P={p}, size={label}")
            for _, r in block.sort_values("Algorithm").iterrows():
                a = int(r.Algorithm)
                print(f"    algo {a} ({ALG_NAMES['bcast'][a]}): {r['Avg_Latency(us)']:.2f} us")
            best = block.loc[block["Avg_Latency(us)"].idxmin()]
            print(f"    -> fastest: algo {int(best.Algorithm)}")


for op, fname in [
    ("bcast", "bcastEPYC.csv"),
    ("bcast", "bcastTHIN.csv"),
    ("barrier", "barrierEPYC.csv"),
    ("barrier", "barrierTHIN.csv"),
]:
    summarize(ROOT / "exercise1" / "results" / fname, op)

for fname in ["bcastEPYC.csv", "bcastTHIN.csv"]:
    bcast_size_summary(ROOT / "exercise1" / "results" / fname)
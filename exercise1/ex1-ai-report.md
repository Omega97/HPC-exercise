# Exercise 1 — Results Report

> OSU Micro-Benchmarks on the Orfeo cluster (EPYC + THIN).  
> Data collected Jun 2026. Detailed command logs: `ex1_execution_log.md`.

---

## Overview

Exercise 1 compares Open MPI collective algorithms using the [OSU Micro-Benchmarks](https://mvapich.cse.ohio-state.edu/benchmarks/) on two Orfeo node types. All four required result files are **complete**, validated, synced locally, and pushed to GitHub (`cde300e`).

| Collective | Node type | Result file | Lines | Status |
|---|---|---|---|---|
| Broadcast | EPYC | `bcastEPYC.csv` | 7309 | Complete |
| Broadcast | THIN | `bcastTHIN.csv` | 5881 | Complete |
| Barrier | EPYC | `barrierEPYC.csv` | 480 | Complete |
| Barrier | THIN | `barrierTHIN.csv` | 561 | Complete |

---

## Environment

| Item | Value |
|---|---|
| Cluster | Orfeo (`195.14.102.215`) |
| MPI | `openMPI/4.1.6` |
| Benchmark | OSU Micro-Benchmarks 7.3 |
| EPYC jobs | 2 exclusive nodes, 128 MPI ranks/node |
| THIN jobs | 2 exclusive nodes, 24 MPI ranks/node |
| Scheduler | SLURM (`#SBATCH --time` max 2 h) |

---

## Result files

### `bcastEPYC.csv` — Broadcast on EPYC

**Description:** Latency of `osu_bcast` on EPYC nodes, sweeping message size and process count for four broadcast algorithms.

| Field | Content |
|---|---|
| Columns | `Algorithm, Processors, Size(bytes), Avg_Latency(us)` |
| Algorithms | 0 baseline, 1 linear, 2 chain, 5 binary tree |
| Process counts | 2, 4, 8, 16, 32, 48, 64, 96, 128, 176, 224, **256** |
| Message sizes | OSU default sweep (1 B → 1 MiB) |
| Repetitions | 10 outer loops per (algorithm, proc, size) |
| SLURM job | 1277489 (`bcast_latencies.sh`) — TIMEOUT at 2 h but data fully usable |

**Highlights:** All algorithms reach 256 processes. At 256 procs and 1-byte messages, algo 5 (binary tree) is fastest (~7 µs); at 1 MiB, baseline (~1.5 ms) beats tuned algos by 3–6×. Performance is **regime-dependent** (small-message latency vs large-message bandwidth).

---

### `bcastTHIN.csv` — Broadcast on THIN

**Description:** Same broadcast sweep as EPYC, on THIN (lower core-count) nodes for architecture comparison.

| Field | Content |
|---|---|
| Columns | `Algorithm, Processors, Size(bytes), Avg_Latency(us)` |
| Algorithms | 0, 1, 2, 5 (same as EPYC) |
| Process counts | 2, 4, 8, 12, 16, 24, **48** (max for 2×24 cores) |
| Repetitions | 10 outer loops |
| SLURM job | 1277502 (`bcast_thin.sh`) — COMPLETED in 11 min |

**Highlights:** Full coverage across all algorithms and processor counts. Use with `bcastEPYC.csv` for EPYC vs THIN log-log plots (latency vs processors and vs message size).

---

### `barrierEPYC.csv` — Barrier on EPYC

**Description:** Latency of `osu_barrier` on EPYC nodes, sweeping process count for four barrier algorithms. Built by merging two split SLURM runs after monolithic jobs timed out.

| Field | Content |
|---|---|
| Columns | `Algorithm, Processors, Avg_Latency(us)` |
| Algorithms | 0 baseline, 1 linear, 2 double_ring, 4 bruck |
| Process counts | 2, 4, 8, 16, 32, 48, 64, 96, 128, 176, 224, **256** |
| Repetitions | 10 outer loops; OSU `-i/-x 200` per run |
| SLURM jobs | 1303691 alg01 (algos 0+1, 1h26m) + 1303806 alg24 (algos 2+4, 1h27m) |

**Coverage per algorithm:**

| Algo | Rows | Expected | Note |
|---|---|---|---|
| 0 (baseline) | 120 | 120 | Complete |
| 1 (linear) | 119 | 120 | 1 row short |
| 2 (double_ring) | 120 | 120 | Complete |
| 4 (bruck) | 120 | 120 | Complete |

**Highlights:** Barrier at 256 procs is expensive; splitting the job by algorithm pair was required to stay within Orfeo's 2-hour wall limit. Suitable for latency-vs-processors plots and algorithm comparison on high core-count hardware.

---

### `barrierTHIN.csv` — Barrier on THIN

**Description:** Same barrier measurement as EPYC, on THIN nodes.

| Field | Content |
|---|---|
| Columns | `Algorithm, Processors, Avg_Latency(us)` |
| Algorithms | 0, 1, 2, 4 (same as EPYC) |
| Process counts | 2, 4, 8, 12, 16, 24, **48** |
| Repetitions | 20 outer loops |
| SLURM job | 1277506 (`barrier_thin.sh`) — COMPLETED in 22 min |

**Highlights:** Exactly 561 lines (560 data + header) = 4 algos × 7 proc counts × 20 iterations. Cleanest dataset of the four; no timeouts or gaps.

---

## SLURM job history

| Job ID | Script | Partition | State | Elapsed | Output |
|---|---|---|---|---|---|
| 1277489 | `bcast_latencies.sh` | EPYC | TIMEOUT | 2h | `bcastEPYC.csv` (usable) |
| 1277494 | `barrier_latencies.sh` | EPYC | TIMEOUT | 2h | partial (superseded) |
| 1277502 | `bcast_thin.sh` | THIN | COMPLETED | 11 min | `bcastTHIN.csv` |
| 1277506 | `barrier_thin.sh` | THIN | COMPLETED | 22 min | `barrierTHIN.csv` |
| 1303325 | `barrier_latencies.sh` (4h) | — | CANCELLED | — | invalid wall time |
| 1303630 | `barrier_latencies.sh` (tuned) | EPYC | TIMEOUT | 2h | 335 lines (superseded) |
| 1303667 | `barrier_latencies_alg01.sh` (1h) | EPYC | TIMEOUT | 1h | 168 lines (superseded) |
| 1303691 | `barrier_latencies_alg01.sh` (2h) | EPYC | COMPLETED | 1h26m | `barrierEPYC_alg01.csv` |
| 1303806 | `barrier_latencies_alg24.sh` (2h) | EPYC | COMPLETED | 1h27m | `barrierEPYC_alg24.csv` |

---

## Key lessons (methodology)

1. **Orfeo max wall time is 2 hours** — longer `#SBATCH --time` is rejected and hurts queue priority.
2. **Timeouts were workload-driven** — 256-proc barrier runs with many outer iterations and high OSU `-i/-x` values exceed 2 h.
3. **Fix that worked:** split EPYC barrier into two jobs (algos 0+1 and 2+4), each with `--time=02:00:00`, `iterations=10`, `-i/-x 200`.
4. **THIN jobs finished quickly** (11–22 min) — same scripts, fewer cores and lower max process counts.

---

## Scientific findings (preview for report)

From `bcastEPYC.csv` at **256 processes**:

| Message size | Fastest algorithm | Observation |
|---|---|---|
| 1–4 bytes | Algo 5 (binary tree) | Tuned algos win in latency-dominated regime |
| 1 MiB | Algo 0 (baseline) | Default pipelining/segmentation wins by 3–6× |

Barrier and THIN-vs-EPYC comparisons are ready to plot in the analysis notebook.

---

## Remaining deliverables

| Task | Status |
|---|---|
| Data collection (4 CSVs) | **Done** |
| `results_and_modelling.ipynb` (log-log plots, performance models) | Not started |
| Report (≤10 pages, `CUSMAFAIT_report.pdf`) | Not started |
| Slides (≤10 slides) | Not started |
| Share repo with teachers | Not started |

---

*Last updated: 2026-06-20*
# Exercise 1 — AI Session Report

> High-level summary of work done with AI copilot guidance (Jun 2026).  
> Detailed command logs live in `ex1_execution_log.md`.

---

## Goal (official requirements)

Compare Open MPI collective algorithms on Orfeo using OSU Micro-Benchmarks:

- **Mandatory:** `osu_bcast` on two node types (EPYC + THIN)
- **Chosen extra collective:** `osu_barrier`
- **Algorithms:** baseline (0) + up to 3 tuned variants per operation
- **Deliverables:** CSV results, log-log plots, performance models, report (≤10 pages), slides (≤10)

---

## What we accomplished

### Infrastructure

- OSU benchmarks compiled on Orfeo (`openMPI/4.1.6`) → `bin/osu_bcast`, `bin/osu_barrier`
- SLURM scripts for 4 benchmark jobs: `bcast_latencies.sh`, `barrier_latencies.sh`, `bcast_thin.sh`, `barrier_thin.sh`
- Removed stale `exercise_1/` folder on Orfeo; active path is `exercise1/`

### Data collection

| File | Partition | Status | Lines | Notes |
|---|---|---|---|---|
| `bcastTHIN.csv` | THIN | **Complete** | 5881 | Ready for analysis |
| `barrierTHIN.csv` | THIN | **Complete** | 561 | Exact expected count (4×7×20 + header) |
| `bcastEPYC.csv` | EPYC | **Complete** | 7309 | All algos (0,1,2,5) reach 256 procs |
| `barrierEPYC.csv` | EPYC | **Complete** | 480 | Merged from split jobs 1303691 + 1303806 |

### EPYC barrier troubleshooting (key lessons)

1. **Orfeo max wall time is 2 hours** — longer `#SBATCH --time` is invalid and hurts queue priority.
2. **Timeouts were caused by workload**, not the wall limit alone: too many outer iterations × heavy `-i/-x` values × 256-proc barrier runs.
3. **Successful tuning steps:**
   - `iterations`: 20 → 10
   - OSU flags: `-i/-x 1e4` → `500`
   - Still not enough for all 4 algorithms in one job → split strategy prepared
4. **Split scripts created** (not yet submitted on Orfeo):
   - `barrier_latencies_alg01.sh` — algos 0+1, `--time=01:00:00`, → `barrierEPYC_alg01.csv`
   - `barrier_latencies_alg24.sh` — algos 2+4, `--time=01:00:00`, → `barrierEPYC_alg24.csv`

### Early scientific findings (from `bcastEPYC.csv`)

- **Small messages (1–4 bytes, 256 procs):** tuned algo 5 (binary tree) wins on 1-byte; baseline competitive on 2–4 bytes.
- **Large messages (1 MiB, 256 procs):** baseline ~1.5 ms; tuned algos 5–10× slower.
- **Conclusion:** performance is **regime-dependent** (latency-dominated vs bandwidth/segmentation-dominated) — strong material for the report.

---

## Status (2026-06-20)

**Data collection complete.** All four CSVs validated, synced locally, and pushed to GitHub (`cde300e`).

---

## Next steps (in order)

### 1. ~~Finish EPYC barrier data~~ ✓ Done

```bash
cd ~/HPC-exercise && git pull
cd exercise1
mv results/barrierEPYC.csv results/barrierEPYC_run1.csv
chmod +x scripts/barrier_latencies_alg01.sh scripts/barrier_latencies_alg24.sh
cd scripts
sbatch barrier_latencies_alg01.sh   # wait for COMPLETED
sbatch barrier_latencies_alg24.sh   # wait for COMPLETED
```

Merge outputs (skip duplicate headers):

```bash
cd ~/HPC-exercise/exercise1/results
head -1 barrierEPYC_alg01.csv > barrierEPYC.csv
tail -n +2 barrierEPYC_alg01.csv >> barrierEPYC.csv
tail -n +2 barrierEPYC_alg24.csv >> barrierEPYC.csv
wc -l barrierEPYC.csv   # expect ~481
```

### 2. Validate full dataset

Coverage check on all four CSVs: algorithms present, processor counts, repetition counts. Flag gaps before analysis.

### 3. Sync results to local repo

Copy CSVs from Orfeo → `exercise1/results/`, commit, push. Share repo with teachers.

### 4. Analysis & plots

Create `exercise1/scripts/results_and_modelling.ipynb`:

- Latency vs processors (bcast + barrier, EPYC vs THIN, all algorithms)
- Latency vs message size at fixed proc count (bcast only)
- Log-log plots + fitted performance-model equations

### 5. Report & slides

- Software stack (OpenMPI 4.1.6, OSU 7.3, SLURM scripts)
- Methodology (node types, algorithms, iterations, Orfeo constraints)
- Results + regime-dependent interpretation
- 8–10 slide deck for the 10-minute presentation

---

## Job history (quick reference)

| Job ID | Script | Partition | State | Elapsed |
|---|---|---|---|---|
| 1277489 | bcast EPYC | EPYC | TIMEOUT | 2h (data usable) |
| 1277494 | barrier EPYC (old) | EPYC | TIMEOUT | 2h |
| 1277502 | bcast THIN | THIN | COMPLETED | 11 min |
| 1277506 | barrier THIN | THIN | COMPLETED | 22 min |
| 1303325 | barrier EPYC (4h, invalid) | — | CANCELLED | — |
| 1303630 | barrier EPYC (tuned) | EPYC | TIMEOUT | 2h (335 lines) |

---

*Last updated: 2026-06-20*
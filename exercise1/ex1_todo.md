
# Exercise 1 Report

---

## TODOs

Based on the exercise requirements and your existing scripts, here is the strategic list of jobs you need to submit to the ORFEO cluster to complete Exercise 1.

The exercise requires:
1.  **Mandatory:** `osu_bcast` (Broadcast).
2.  **Choice:** One additional collective (`barrier`, `gather`, `scatter`, or `reduce`). *Your scripts currently use `barrier`.*
3.  **Nodes:** You must test on at least two different node types (e.g., **EPYC** and **THIN**).
4.  **Algorithms:** For each operation, compare the **Baseline (0)** against **up to 3 specific algorithms**.

### 📋 The Job Submission List

You need to submit **4 distinct SLURM jobs** to cover the mandatory requirements across two architectures.

| Job ID | Script Name | Target Node Type | Collective Op | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `bcast_epyc.sh` | **EPYC** | `bcast` | Mandatory broadcast baseline + algos on high-core count nodes. |
| **2** | `bcast_thin.sh` | **THIN** | `bcast` | Mandatory broadcast baseline + algos on low-core count nodes. |
| **3** | `barrier_epyc.sh` | **EPYC** | `barrier` | Your chosen secondary operation on high-core count nodes. |
| **4** | `barrier_thin.sh` | **THIN** | `barrier` | Your chosen secondary operation on low-core count nodes. |

---

### 🛠️ How to Prepare the Scripts

You already have `bcast_latencies.sh` and `barrier_latencies.sh`. You need to create copies and modify the **SLURM headers** for the THIN nodes.

#### 1. For EPYC Nodes (Use your current scripts)
*   **File:** `scripts/bcast_epyc.sh` (Copy of `bcast_latencies.sh`)
    *   Ensure `#SBATCH --partition=EPYC`
    *   Ensure `#SBATCH --ntasks-per-node=128`
*   **File:** `scripts/barrier_epyc.sh` (Copy of `barrier_latencies.sh`)
    *   Ensure `#SBATCH --partition=EPYC`
    *   Ensure `#SBATCH --ntasks-per-node=128`
   
#### 2. For THIN Nodes (Create new versions)
*   **File:** `scripts/bcast_thin.sh`
    *   Change `#SBATCH --job-name=ex1THINbc`
    *   Change `#SBATCH --partition=THIN`
    *   Change `#SBATCH --ntasks-per-node=24` *(Thin nodes usually have fewer cores)*
    *   Update `number_processors` array to match Thin capacity (e.g., `2 4 8 12 24 48`).
    *   Update `output_file` to `"${output_dir}bcastTHIN.csv"`
*   **File:** `scripts/barrier_thin.sh`
    *   Change `#SBATCH --job-name=ex1THINarr`
    *   Change `#SBATCH --partition=THIN`
    *   Change `#SBATCH --ntasks-per-node=24`
    *   Update `number_processors` array.
    *   Update `output_file` to `"${output_dir}barrierTHIN.csv"`

> **Note:** Check the exact core count of THIN nodes on ORFEO using `sinfo -p THIN -o "%N %c"` before setting `--ntasks-per-node`.

---

### 🚀 Execution Steps on ORFEO

1.  **Compile OSU Benchmarks (Once):**
    ```bash
    cd scripts
    chmod +x make.sh
    ./make.sh  # Or run the commands manually if make.sh is just a text file
    ```

2.  **Submit the 4 Jobs:**
    ```bash
    sbatch scripts/bcast_epyc.sh
    sbatch scripts/bcast_thin.sh
    sbatch scripts/barrier_epyc.sh
    sbatch scripts/barrier_thin.sh
    ```

3.  **Monitor Progress:**
    ```bash
    squeue -u $USER
    ```

4.  **Retrieve Results:**
    Once finished, check the `results/` folder. You should have:
    *   `bcastEPYC.csv`
    *   `bcastTHIN.csv`
    *   `barrierEPYC.csv`
    *   `barrierTHIN.csv`

### 📊 Post-Processing (For your Report)
After downloading the CSVs, your Python analysis script should:
1.  **Plot 1:** Latency vs. Processors for `bcast` (EPYC vs. THIN) for all algorithms.
2.  **Plot 2:** Latency vs. Processors for `barrier` (EPYC vs. THIN) for all algorithms.
3.  **Plot 3 (Optional but recommended):** Latency vs. Message Size for `bcast` (fixed processor count, e.g., 128) to show the "performance model" mentioned in the exercise.

This approach ensures you meet all criteria: mandatory `bcast`, one choice (`barrier`), two node types (`EPYC`/`THIN`), and algorithm comparison.

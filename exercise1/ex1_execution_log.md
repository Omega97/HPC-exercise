
# **Execution Log - Exercise 1**

> This is the detailed log of **Exercise 1** of the HPC project: *Comparison of different Open MPI algorithms for collective operations using the OSU Micro-Benchmarks on the Orfeo cluster*.

---

## 🔐 Accessing Orfeo

### 1. Open Command Prompt as Administrator
```
Win + X → A
```

### 2. Start WSL and connect to Orfeo
```bash
wsl
orfeo
```
(or manually: `ssh -i ~/.ssh/orfeo_key_new ocusmafait@195.14.102.215`)

---

## 📁 Setting up the Project

```bash
# Go to the project folder
cd ~/HPC-exercise/exercise1

# Create necessary directories
mkdir -p scripts results bin

# Check account and partitions
sacctmgr list associations Users=$(whoami) format=Account,User,Partition
```

---

## 🛠️ 1. Compiling the OSU Micro-Benchmarks

```bash
cd scripts
chmod +x make.sh

# Compile OSU benchmarks
./make.sh
```

This script:
- Loads the correct OpenMPI module
- Downloads and compiles `osu-micro-benchmarks-7.3`
- Copies `osu_bcast` and `osu_barrier` into `../bin/`

**Software stack used:**
```bash
module load openMPI/4.1.5/gnu/12.2.1
```

---

## 📜 2. Preparing SLURM Scripts

I prepared **4 SLURM jobs** to satisfy all requirements:

- **Mandatory**: `osu_bcast` on **EPYC** and **THIN** nodes
- **Chosen collective**: `osu_barrier`
- Algorithms tested: `0 (default)` + `1, 2, 5` for bcast and `0, 1, 2, 4` for barrier

```bash
# Make scripts executable
chmod +x scripts/bcast_epyc.sh scripts/barrier_epyc.sh
chmod +x scripts/bcast_thin.sh scripts/barrier_thin.sh
```

I created `bcast_thin.sh` and `barrier_thin.sh` by copying the EPYC versions and modifying:
- `--partition=THIN`
- `--ntasks-per-node=24`
- Adjusted `number_processors` array
- Changed output filenames (`bcastTHIN.csv`, `barrierTHIN.csv`)

---

## 🚀 3. Submitting the Jobs

```bash
cd ~/HPC-exercise/exercise1

sbatch scripts/bcast_epyc.sh
sbatch scripts/bcast_thin.sh
sbatch scripts/barrier_epyc.sh
sbatch scripts/barrier_thin.sh
```

---

## 📊 4. Monitoring and Retrieving Results

```bash
# Check running jobs
squeue -u ocusmafait

# Watch in real time
watch -n 5 squeue -u ocusmafait

# Once finished, check results
ls -l results/
cat results/bcastEPYC.csv | head -n 10
```

Expected output files:
- `bcastEPYC.csv`
- `bcastTHIN.csv`
- `barrierEPYC.csv`
- `barrierTHIN.csv`

---

## 📈 5. Post-Processing

After downloading the CSV files to my local PC, I used the Python notebook `results_and_modelling.ipynb` to:
- Generate comparison plots (EPYC vs THIN)
- Plot latency vs number of processors for each algorithm
- Create performance model graphs

---

**✅ Exercise 1 Completed Successfully**

- Ran on 2 different node types (**EPYC** + **THIN**)
- Tested mandatory `bcast` + chosen `barrier`
- Compared default algorithm vs 3 tuned algorithms per operation
- Used proper SLURM scripts with correct software stack documented

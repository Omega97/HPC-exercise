
# **Execution Log - Exercise 2c (The Mandelbrot Set)**

> This is the detailed log of **Exercise 2c** of the HPC project: *Parallel implementation of the Mandelbrot set using a hybrid MPI + OpenMP approach on the Orfeo cluster*.

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

---

## 📁 1. Navigating to the Project

```bash
cd ~/HPC-exercise/exercise2

# Check current directory and account
pwd
sacctmgr list associations Users=$(whoami) format=Account,User,Partition
```

---

## 🛠️ 2. Building the Executable

```bash
# Load the correct module
module load openMPI/4.1.5/gnu/12.2.1

# Make the build script executable and run it
cd scripts
chmod +x make.sh

# Option -a = load module | Option -b = build with CMake
./make.sh -a -b
```

**What we expect back:**
- Successful CMake configuration and build
- Message: `✅ Executable successfully created in the build/bin directory.`
- The binary is located at: `../build/bin/mandelbrot`

---

## 🚀 3. Submitting the Scaling Jobs

I submitted **4 SLURM jobs** to properly evaluate strong and weak scaling (both MPI and OpenMP parts):

```bash
cd ~/HPC-exercise/exercise2

sbatch scripts/strong_scaling_MPI_EPYC.sh
sbatch scripts/strong_scaling_OMP_EPYC.sh
sbatch scripts/weak_scaling_MPI_EPYC.sh
sbatch scripts/weak_scaling_OMP_EPYC.sh
```

**What these jobs do:**
- `strong_scaling_MPI_EPYC.sh` → Fixed problem size, increasing MPI processes (up to 256)
- `strong_scaling_OMP_EPYC.sh` → Fixed problem size, increasing OpenMP threads (1 to 64)
- `weak_scaling_MPI_EPYC.sh` → Increasing both problem size and MPI processes
- `weak_scaling_OMP_EPYC.sh` → Increasing both problem size and OpenMP threads

---

## 📊 4. Monitoring the Jobs

```bash
# Check my jobs
squeue -u ocusmafait

# Real-time monitoring
watch -n 5 squeue -u ocusmafait

# Check a specific job details
sacct -j <JOBID> --format=JobID,JobName,Partition,Elapsed,State
```

---

## 📥 5. Retrieving Results

Once the jobs are completed (`State: COMPLETED`):

```bash
ls -l results/
ls -l plots/

# Check content of results
head -n 5 results/strong_scaling_MPI_EPYC.csv
head -n 5 results/weak_scaling_OMP_EPYC.csv
```

**Expected output files:**
- `results/strong_scaling_MPI_EPYC.csv`
- `results/strong_scaling_OMP_EPYC.csv`
- `results/weak_scaling_MPI_EPYC.csv`
- `results/weak_scaling_OMP_EPYC.csv`
- `plots/mandelbrot_set.pgm` (and `.png`)
- Various scaling plots (strong/weak, hybrid)

---

## 📈 6. Post-Processing & Visualization

After downloading the results to my local computer (via `scp` or WinSCP):

- I ran the Python analysis script / Jupyter notebook to generate:
  - Strong Scaling plots (MPI vs OpenMP)
  - Weak Scaling plots
  - Hybrid scaling comparison
  - Mandelbrot set image (`mandelbrot_set.png`)

---

**✅ Exercise 2c Completed Successfully**

- Implemented hybrid MPI + OpenMP version of the Mandelbrot set
- Performed both **strong** and **weak** scaling analysis
- Generated correct `.pgm` image output
- Produced all required performance plots
- Documented the software stack (`openMPI/4.1.5/gnu/12.2.1` + CMake + GCC)

# HPC-exercise
HPC Exercise

**High-Performance Computing Exam Project – 2023/2024**  
**Student: Omar Cusma Fait**

---

## Connect to Orfeo

1) Fire up Command Prompt as Admin `Win + X -> A`

2) Run WSL (Windows Subsystem for Linux)
```
wsl
```

3) Connect
```
ssh -i ~/.ssh/orfeo_key ocusmafait@195.14.102.215
```

---

## Deliverables

The exam consists of:

- [HPC Project Github repo](https://github.com/Omega97/HPC-exercise)

  1) [Exercise_1](exercise_1.md): Compare different Open MPI algorithms for collective operations.
  2) [Exercise_2](exercise_2.md): Implement a broadcast algorithm or a all-to-all algorithm in distributed memory

- Project Report #todo link

- Presentation of the exercise (PPT) #todo link

---

## 📌 **PROJECT SUMMARY**

This repository contains the complete work for the **HPC part of the exam** (Prof. Cozzini’s section).  
The exam is split into **two independent exercises**:

| Exercise                        | Type                                                                                    | Status          |
|---------------------------------|-----------------------------------------------------------------------------------------|-----------------|
| **[Exercise_1](exercise_1.md)** | **Benchmarking Open MPI collective algorithms** (Broadcast + one additional collective) | **IN PROGRESS** |
| **[Exercise_2](exercise_2.md)** | **Parallel implementation of a computational kernel** (choice: 2a/2b + 2c or hybrid 2c) | **NOT STARTED** |

> **Chosen path for Exercise 2**:  
> - **MPI-only** for **2a (custom Broadcast)**  
> - **OpenMP-only** for **2c (Mandelbrot set)**  
> *(Hybrid MPI+OpenMP version of 2c is optional and not currently planned)*

---

## TODO

- [x] Cloned starter repo from `Omega97/HPC-exercise`
- [x] Created local project structure on `C:\Users\monfalcone\PycharmProjects\HPC-exercise`
- [x] Drafted initial `README.md` with project plan and timeline
- [x] Added personal notes:  
  - `data/notes/exercise_notes.md`  
  - `data/notes/orfeo.md`
- [x] Downloaded and extracted OSU Micro-Benchmarks v7.3 from [MVAPICH site](https://mvapich.cse.ohio-state.edu/benchmarks/)
- [x] Confirmed SSH access to ORFEO cluster:  
  ```bash
  ssh ocusmafait@195.14.102.215
  ```
- [x] Tested login and navigation on login node
- [x] Created `exercise1/osu-micro-benchmarks-7.3/` directory

---

## EXERCISE 1: Open MPI Collective Benchmarking – TO-DO LIST

### Setup & Environment
- [ ] Load correct modules on ORFEO:
  ```bash
  module load intel/2023
  module load openmpi/4.1.5-intel
  ```
- [ ] Verify Open MPI version and `coll tuned` parameters:
  ```bash
  ompi_info --param coll all --level 9
  ```
- [ ] Create `exercise1/scripts/slurm/` directory

### Compile OSU Benchmarks
- [ ] Compile OSU benchmarks locally on ORFEO:
  ```bash
  cd exercise1/osu-micro-benchmarks-7.3
  ./configure CC=mpicc CXX=mpicxx --prefix=$(pwd)
  make && make install
  ```
- [ ] Verify binaries exist in `c/mpi/collective/blocking/`:
  - `osu_bcast`
  - `osu_reduce`

### Select Resources
- [ ] Request **2 full Epyc nodes** (128 cores each → 256 total MPI ranks)
  ```bash
  #SBATCH --partition=EPYC
  #SBATCH --nodes=2
  #SBATCH --ntasks-per-node=128
  #SBATCH --cpus-per-task=1
  ```

### Baseline Runs (Default Algorithm)
- [ ] Run `osu_bcast` with high iterations:
  ```bash
  mpirun ./osu_bcast -i 1000 -x 200 > data/bcast_default_256p.txt
  ```
- [ ] Run `osu_reduce` (chosen collective):
  ```bash
  mpirun ./osu_reduce -i 1000 -x 200 > data/reduce_default_256p.txt
  ```

### Algorithm Variants
#### Broadcast (3 algorithms)
- [ ] Pipeline (`--mca coll_tuned_bcast_algorithm 3`)
- [ ] Binary Tree (`5`)
- [ ] Binomial (`6`)

#### Reduce (3 algorithms)
- [ ] Rabenseifner (`7`)
- [ ] Binary (`4`)
- [ ] Linear (`1`)

> Run each with:
> ```bash
> --mca coll_tuned_use_dynamic_rules true
> ```

### Point-to-Point Latency
- [ ] Measure intra-socket (cores 0–1):
  ```bash
  mpirun -np 2 --cpu-list 0,1 ./osu_latency > data/latency_intra.txt
  ```
- [ ] Measure inter-socket (cores 0–8):
  ```bash
  mpirun -np 2 --cpu-list 0,8 ./osu_latency > data/latency_inter.txt
  ```

### Data Collection
- [ ] Create `exercise1/data/` and save all `.txt` outputs
- [ ] Write Python parser to extract `Size` and `Avg Latency(us)`
- [ ] Generate log-log plots (Matplotlib)

### Performance Modeling
- [ ] Derive α (latency) and β (bandwidth) from `osu_latency`
- [ ] Build naive model for:
  - Pipeline Bcast: `T = α * (P-1) + β * M`
  - Binary Tree: `T ≈ α * log₂(P) + β * M`
- [ ] Compare model vs measured data

---

## EXERCISE 2: Parallel Algorithms – TO-DO LIST

### Exercise 2a: Custom MPI Broadcast
- [ ] Create `exercise2/2a_custom_bcast/`
- [ ] Implement `my_bcast_pipeline(void* data, int count, MPI_Datatype dtype, int root, MPI_Comm comm)`
  - Use `MPI_Send` / `MPI_Recv` in a chain
- [ ] Implement `my_bcast_binary_tree(...)`
- [ ] Write test program comparing:
  - `MPI_Bcast`
  - `my_bcast_pipeline`
  - `my_bcast_binary_tree`
- [ ] Validate correctness (same data on all ranks)

### Exercise 2c: OpenMP Mandelbrot
- [ ] Create `exercise2/2c_mandelbrot_omp/`
- [ ] Write `mandelbrot.c` with:
  - CLI: `./mandelbrot nx ny xL yL xR yR Imax`
  - Default: `1920 1080 -2.0 -1.4 0.8 1.4 1000`
  - Use `short int` matrix (`I_max ≤ 65535`)
- [ ] Parallelize with:
  ```c
  #pragma omp parallel for schedule(dynamic, 64)
  ```
- [ ] Integrate `write_pgm_image()` from Appendix I
- [ ] Output: `mandelbrot.pgm`

### Scaling Studies

#### OpenMP (2c)
- [ ] Write `scaling/omp_strong.sh`:
  - Fixed problem: `3840x2160`, `I_max=5000`
  - Vary threads: 1, 2, 4, ..., 128
- [ ] Write `scaling/omp_weak.sh`:
  - Work per thread fixed → scale image with threads

#### MPI (2a)
- [ ] Write `scaling/mpi_strong.sh`:
  - Fixed message size (e.g., 1MB), vary ranks: 2, 4, ..., 256
- [ ] Compare `MPI_Bcast` vs `my_bcast_*`

---

## BUILD & RUN INSTRUCTIONS (DRAFT)

```bash
# On ORFEO
module load intel/2023 openmpi/4.1.5-intel

# Exercise 1: Compile OSU
cd exercise1/osu-micro-benchmarks-7.3
./configure CC=mpicc CXX=mpicxx --prefix=$(pwd)
make -j8 && make install

# Submit job
sbatch exercise1/scripts/slurm/run_bcast_default.sbatch
```

---

## DELIVERABLES CHECKLIST

- [ ] GitHub repo shared with `luca.tornatore@inaf.it` and `stefano.cozzini@areasciencepark.it`  
- [ ] `YOURSURNAME_report.pdf` (≤10 pages)  
- [ ] PPT presentation (≤10 slides)  
- [ ] All scripts use `Makefile` or SLURM  
- [ ] Log-log performance plots  
- [ ] Performance models with equations  
- [ ] Correctness proof: `my_bcast == MPI_Bcast`  
- [ ] `.pgm` images from Mandelbrot  

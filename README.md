
# HPC-exercise 💻

HPC Exercise

**High-Performance Computing Exam Project – 2023/2024**  
**Student: Omar Cusma Fait**

---

## Connect to Orfeo

1) Fire up the Command Prompt as Admin `Win + X -> A`
2) Run WSL (Windows Subsystem for Linux)`wsl`
3) Connect `ssh -i ~/.ssh/orfeo_key ocusmafait@195.14.102.215`

---

## Deliverables

Implement the following exercises provided by the professors:

- [ ] [HPC Project Github repo](https://github.com/Omega97/HPC-exercise)

  1) [Exercise_1](PUBLIC/exercise_1.md): Compare different Open MPI algorithms for collective operations.
  2) [Exercise_2](PUBLIC/exercise_2.md): Implement a broadcast algorithm or a all-to-all algorithm in distributed memory

- [ ] [Exercise 1 Report](PUBLIC/report/CUSMAFAIT_report.pdf) (≤10 pages)  
- [ ] [Exercise 1 Presentation](PUBLIC/report/CUSMAFAIT_slides.pdf) (≤10 slides) 


- [ ] share GitHub repo with `luca.tornatore@inaf.it` and `stefano.cozzini@areasciencepark.it`  
- [ ] All scripts use `Makefile` or SLURM  
- [ ] Log-log performance plots  
- [ ] Performance models with equations  
- [ ] Correctness proof: `my_bcast == MPI_Bcast`  
- [ ] `.pgm` images from Mandelbrot  


---

## 📌 **PROJECT SUMMARY**

This repository contains the complete work for the **HPC part of the exam** (Prof. Cozzini’s section).  
The exam is split into **two independent exercises**:

| Exercise                                | Type                                                                                    | Status          |
|-----------------------------------------|-----------------------------------------------------------------------------------------|-----------------|
| **[Exercise_1](PUBLIC/exercise_1.md)** | **Benchmarking Open MPI collective algorithms** (Broadcast + one additional collective) | **IN PROGRESS** |
| **[Exercise_2](PUBLIC/exercise_2.md)** | **Parallel implementation of a computational kernel** (choice: 2a/2b + 2c or hybrid 2c) | **NOT STARTED** |

> **Chosen path for Exercise 2**:  
> - **MPI-only** for **2a (custom Broadcast)**  
> - **OpenMP-only** for **2c (Mandelbrot set)**  
> *(Hybrid MPI+OpenMP version of 2c is optional and not currently planned)*

---

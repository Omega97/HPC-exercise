
# HPC-exercise 💻

HPC Exercise

**High-Performance Computing Exam Project – 2023/2024**  
**Student: Omar Cusma Fait**

> L'appello successivo è per il 15 di luglio.  Esse3 l'appello per il codice 345SM.  

---

## Connect to Orfeo

1) Fire up the Command Prompt as Admin `Win + X -> A`
2) Run WSL (Windows Subsystem for Linux)`wsl`
3) Connect `ssh -i ~/.ssh/orfeo_key ocusmafait@195.14.102.215`
   - (or just `orfeo` if the shortcut is set up)

---

## Deliverables

Implement the following exercises provided by the professors:

- [ ] [HPC Project Github repo](https://github.com/Omega97/HPC-exercise)

  1) [Exercise_1](exercise_1%20-%20official.md): Compare different Open MPI algorithms for collective operations.
  2) [Exercise_2](exercise_2%20-%20official.md): Implement a broadcast algorithm or a all-to-all algorithm in distributed memory

- [ ] [Exercise 1 Report](PUBLIC/repor[results_and_modelling.ipynb](exercise1/scripts/results_and_modelling.ipynb)t/CUSMAFAIT_report.pdf) (≤10 pages)  
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

| Exercise                               | Type                                                                                    |
|----------------------------------------|-----------------------------------------------------------------------------------------|
| **[Exercise_1](exercise_1%20-%20official.md)** | **Benchmarking Open MPI collective algorithms** (Broadcast + one additional collective) |
| **[Exercise_2](exercise_2%20-%20official.md)** | **Parallel implementation of a computational kernel** (choice: 2a/2b + 2c or hybrid 2c) |

> **Chosen path for Exercise 2**:  
> - **MPI-only** for **2a (custom Broadcast)**  
> - **OpenMP-only** for **2c (Mandelbrot set)**  
> *(Hybrid MPI+OpenMP version of 2c is optional and not currently planned)*

---

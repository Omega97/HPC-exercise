## REPOSITORY STRUCTURE

```
HPC-exercise/
├── data/
│   ├── images
│   │   └── ...
│   └── notes/
│       ├── exercise_notes.md
│       └── orfeo.md
├── exercise1/
│   ├── osu-micro-benchmarks-7.3/
│   ├── scripts/
│   │   └── slurm/
│   │       ├── run_bcast.sh
│   │       ├── run_reduce.sh
│   │       └── job_template.sbatch
│   ├── data/
│   │   ├── bcast_default_256p.txt
│   │   ├── latency_intra.txt
│   │   └── ...
│   └── analysis/
│       └── plot_collective.py
├── exercise2/
│   ├── 2a_custom_bcast/
│   │   ├── my_bcast.c
│   │   ├── test_bcast.c
│   │   └── Makefile
│   ├── 2c_mandelbrot_omp/
│   │   ├── mandelbrot.c
│   │   ├── write_pgm_image.c
│   │   └── Makefile
│   └── scaling/
│       ├── omp_strong.sh
│       ├── omp_weak.sh
│       ├── mpi_strong.sh
│       └── plot_scaling.py
├── presentation/
│   └── HPC_presentation.pptx       ← ≤10 slides
├── report/
│   └── YOURSURNAME_report.pdf      ← Final PDF (≤10 pages)
├── .gitignore
├── exercise_1.md
├── exercise_2.md
├── main.py
├── project_description.py
├── project_structure.py
├── Makefile
└── README.md
```

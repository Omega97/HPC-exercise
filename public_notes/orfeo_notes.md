# Orfeo Notes

---

## Orfeo Specs

Orfeo Cluster

AMD - Intel - GPU Nodes

AND Epyc nodes

### Orfeo documentation

SLURM: open source job scheduler 

https://orfeo-doc.areasciencepark.it/HPC/SLURM-basics/

https://orfeo-doc.areasciencepark.it/HPC/SLURM-basics/#run-without-prior-allocation

squeue, salloc (slurm allocate) , sbatch (to run programs)

2h limit allocation for students (you can ask for more by email)

---

```
ssh-keygen -t ecdsa -b 521
ssh-keygen -f ~/tatu-key-ecdsa -t ecdsa -b 521
ssh-copy-id -i ~/.ssh/tatu-key-ecdsa user@host
/etc/ssh/ssh_host_ecdsa_key
```


cluster = login node + compute node + node for storage + ...

login node = allows to enter and do processing, but not a lot of computation
compute node = allows for computation 

```
Esc :wq 	(write quit)
Esc :7 		(go to row)
Esc dd 		(delete line)
Esc u 		(undo)
Esc Ctrl+R 	(redo)
Esc i 		(insert mode)
```

use Nano


programs on login node should be small

```
cat
ls -lrt
mkdir
module avail
python [file_name]
pwd
touch
vi

vi known_host
vi address_key
paste new public key
```

submit jobs with SLURM (run in parallel)

#!/bin/bash
specify time, memory, machine, directory from which you lounch the job
mail to user
sbatch 	[name.job] (submit job)

2h limit, max 2 cores, max 1 job at the time

squeue 			(all submitted jobs)
scancel [name] 		(kill program)

salloc <>

main/PARALLELISM/slurm


### update local github project 

```
cd <folder>
git pull
```

### module system navigation

modules list
module avail
module purge
module load <module_name>

q (to exit)


### youtube slurm tutorial
https://slurm.schedmd.com/overview.html


### compile MPI program
mpicc


PARALLEL_PROGRAMMING/basic-mpi-codes


---

module load openMPI/4.1.5/gnu

### allocate resources <tasks> <cpus> <p?> <name?> <time hh:mm:ss> <memory>
`salloc -n4 --cpus-per-task=2  -p EPYC  --time=00:05:00 --mem=10GB`

### compile + file
`mpicc mpi_hello_world.c -g3 -o mpi_hello_world.x`

### run
`mpirun -np 2 ./mpi_hello_world.x`


to generate different random numbers on each process you can use the processor id as a seed


Limit 200 GB, check with 
`myquota`

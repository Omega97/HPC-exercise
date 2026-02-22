
# Note Esercizio 1

- Usare OSU Micro-Benchmarks, suite di strumenti per misurare le prestazioni di Open MPI
- Testare **MPI_Bcast** (la funzione di MPI che fa effettivamente il broadcast)
- Girare le benchmark su ORFEO, usando almeno due nodi **interi** (usare tutti i cores)
- Scegliere il tipo di nodi, tra **epyc, thin, or fat**
- Abilitare la modifica della scelta dell'algoritmo da usare
```bash
--mca coll_tuned_use_dynamic_rules true
```
- Comparare l'algoritmo di default (algorithm=0) con al meno 2 o 3 altri algoritmi a scelta (tra binary tree, binomial tree, pipeline, ...)

---

## In pratica

5 jobs totali:

- osu_bcast default (256p) → baseline
- osu_bcast binomial (alg 6)
- osu_bcast pipeline (alg 3)
- osu_reduce default
- osu_reduce rabenseifner (alg 7) ← è quasi sempre il migliore


### Job 1 - osu-micro-benchmarks osu_bcast default

```bash
cd ~/HPC-exercise/exercise_1
```

Il primo benchmark eseguito su 256 processi (2 nodi EPYC completi, 128 core/nodo) con l’algoritmo di broadcast scelto automaticamente da Open MPI ha prodotto la baseline di riferimento.
```bash
cat > scripts/slurm/osu_bcast_default_256p.sbatch << 'EOF'
#!/bin/bash
#SBATCH --job-name=bcast_def_256p
#SBATCH --partition=EPYC
#SBATCH -A dssc
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1[pasgen_omar_fait_v2025.py](../../../../../scripts/pasgen_omar_fait_v2025.py)
#SBATCH --exclusive
#SBATCH --time=00:20:00
#SBATCH --output=../results/bcast_def_256p_%j.out
#SBATCH --error=../results/bcast_def_256p_%j.err

module purge
module load intel/2023 openmpi/4.1.5-intel

cd $SLURM_SUBMIT_DIR/osu-micro-benchmarks-7.3

# Compila solo la prima volta
[ -f c/mpi/collective/blocking/osu_bcast ] || {
  ./configure CC=mpicc CXX=mpicxx --prefix=$(pwd)
  make -j32
  make install
}

mkdir -p ../results

echo "=== OSU MPI_Bcast default algorithm – 256 processi – $(date) ==="

mpirun -np 256 \
  --mca coll_tuned_use_dynamic_rules true \
  ./c/mpi/collective/blocking/osu_bcast \
  -x 1000 -i 1000 \
  > ../results/osu_bcast_default_256p.txt

echo "=== FINITO ==="
EOF
```

sbatch
```
sbatch scripts/slurm/osu_bcast_default_256p.sbatch
```

```
squeue
watch -n 30 squeue -j 708055
```

confirm results
```
tail -n 50 ../results/osu_bcast_default_256p.txt
```
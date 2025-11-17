
## Connect to Orfeo

1) Fire up Command Prompt as Admin `Win + X -> A`

2) Run WSL
```
wsl
```

3) Connect to Orfeo
```
ssh -i ~/.ssh/orfeo_key ocusmafait@195.14.102.215
```

Vai nella cartella del progetto, crea la cartella dell'esercizio, e git-clona il repo
```
cd ~/HPC-exercise/exercise_1
mkdir -p ~/HPC-exercise && cd ~/HPC-exercise
git clone https://github.com/Omega97/HPC-exercise.git
```

Install OSU also on Orfeo
*(OSU = pacchetto di test standard per misurare le prestazioni di MPI)*
```
wget https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz
tar -xzf osu-micro-benchmarks-7.3.tar.gz
rm osu-micro-benchmarks-7.3.tar.gz
```


### Sbatchare il job

Crea lo script SLURM
```
cd ~/HPC-exercise/exercise_1
mkdir -p scripts/slurm data
```

Crea lo script per sbatchare test_matmul
```
cat > scripts/slurm/test_matmul.sbatch << 'EOF'
#!/bin/bash
#SBATCH --job-name=test_matmul
#SBATCH --partition=EPYC
#SBATCH -A dssc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=00:05:00
#SBATCH --output=../data/test_matmul_%j.out
#SBATCH --error=../data/test_matmul_%j.err

module purge
module load intel/2023
module load python/3.11

echo "=== Test Matrix Multiplication ==="
echo "Nodo: $(hostname)"
echo "Data/Ora: $(date)"
echo "CPU disponibili: $SLURM_CPUS_PER_TASK"
echo

python3 matrix_multiplication.py

echo
echo "=== TEST COMPLETATO ==="
EOF
```

Lancia il job
```
sbatch scripts/slurm/run_bcast_default.sbatch
```

Monitora il job (`Ctrl + C` per uscire)
```
watch -n 5 squeue -u $USER
```

Controlla i risultati! 
```
cat ../data/test_matmul_690425.out
```


Git-pusha le modifiche
```
cd ~/HPC-exercise
git add exercise_1/matrix_multiplication.py
git add exercise_1/scripts/slurm/test_matmul.sbatch
git add exercise_1/data/test_matmul_690431.out
git commit -m "Add working matrix multiplication benchmark + real ORFEO results (519 GFLOPS @ 8000×8000)"
git push
```

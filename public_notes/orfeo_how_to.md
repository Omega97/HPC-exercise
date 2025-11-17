
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
cd ~/HPC-exercise/HPC-exercise/exercise1
mkdir -p ~/HPC-exercise && cd ~/HPC-exercise
git clone https://github.com/Omega97/HPC-exercise.git
cd ~/HPC-exercise/HPC-exercise/exercise1
```

Install OSU also on Orfeo
*(OSU = pacchetto di test standard per misurare le prestazioni di MPI)*
```
wget https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz
tar -xzf osu-micro-benchmarks-7.3.tar.gz
rm osu-micro-benchmarks-7.3.tar.gz
```


### Crea lo script SLURM
```
cd ~/HPC-exercise/HPC-exercise/exercise1
```

Crea los cript
```
cat > scripts/slurm/run_bcast_default.sbatch << 'EOF'
#!/bin/bash
#SBATCH --job-name=bcast_def
#SBATCH --partition=epyc
#SBATCH -A dssc
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --exclusive
#SBATCH --time=00:30:00
#SBATCH --output=../data/bcast_def_%j.out
#SBATCH --error=../data/bcast_def_%j.err

module purge
module load intel/2023 openmpi/4.1.5-intel

cd $SLURM_SUBMIT_DIR/osu-micro-benchmarks-7.3

if [ ! -f c/mpi/collective/blocking/osu_bcast ]; then
  echo "Compilazione OSU..."
  ./configure CC=mpicc CXX=mpicxx --prefix=$(pwd) > ../data/configure.log 2>&1
  make -j8 > ../data/make.log 2>&1
  make install > ../data/install.log 2>&1
fi

mkdir -p ../data

echo "Avvio benchmark..."
mpirun -np 256 ./c/mpi/collective/blocking/osu_bcast -i 1000 -x 200 > ../data/bcast_default_256p.txt

echo "Fatto!"
EOF
```

Lancia il job
```
sbatch scripts/slurm/run_bcast_default.sbatch
```

Monitora il job
```
watch -n 5 squeue -u $USER
```

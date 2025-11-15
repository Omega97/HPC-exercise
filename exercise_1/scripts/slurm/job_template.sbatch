#!/bin/bash
#SBATCH --job-name=osu_benchmark
#SBATCH --partition=EPYC
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --exclusive

# Load modules
module purge
module load intel/2023
module load openmpi/4.1.5-intel

# Go to OSU directory
cd /your/path/to/HPC-exercise/exercise1/osu-micro-benchmarks-7.3

# Compile (first run only)
if [ ! -f c/mpi/collective/blocking/osu_bcast ]; then
    echo "Compiling OSU benchmarks..."
    ./configure CC=mpicc CXX=mpicxx --prefix=$(pwd)
    make -j8
    make install
fi

# Run benchmark (example: bcast default)
mpirun -np 256 ./c/mpi/collective/blocking/osu_bcast -i 1000 -x 200 > ../data/bcast_default_256p.txt

echo "Benchmark completed."

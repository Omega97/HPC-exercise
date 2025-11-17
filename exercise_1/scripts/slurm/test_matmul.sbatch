#!/bin/bash
#SBATCH --job-name=test_matmul
#SBATCH --partition=EPYC
#SBATCH -A dssc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=00:10:00
#SBATCH --output=../data/test_matmul_%j.out
#SBATCH --error=../data/test_mat

module purge
module load intel/2023
module load python/3.11

echo "=== TEST PRODOTTO MATRICIALE ==="
echo "Nodo: $(hostname)"
echo "Data/Ora: $(date)"
echo "CPU disponibili: $SLURM_CPUS_PER_TASK"
echo

# Test con diverse dimensioni
python3 matrix_multiplication.py 1000
python3 matrix_multiplication.py 2000
python3 matrix_multiplication.py 4000
python3 matrix_multiplication.py 6000
python3 matrix_multiplication.py 8000

echo
echo "=== TUTTI I TEST COMPLETATI ==="

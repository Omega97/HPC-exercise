#!/bin/bash
#SBATCH --job-name=ex2Smoke
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=smoke_epyc.%j.out
#SBATCH --error=smoke_epyc.%j.err
#SBATCH --time=00:10:00
#SBATCH --partition=EPYC
#SBATCH --nodelist=epyc003

# Quick validation: build, run small image, write PGM.

cd "$(dirname "$0")" || exit 1
bash make.sh -b

executable="../build/bin/mandelbrot"
output_image="../plots/mandelbrot_set.pgm"
mkdir -p ../plots

export OMP_NUM_THREADS=4
export OMP_PLACES=cores
export OMP_PROC_BIND=close

"${executable}" 200 200 -2.0 -1.0 0.5 1.0 255 "${output_image}"

job_id=$SLURM_JOB_ID
echo "Job Statistics for Job ID $job_id:"
sacct -j "$job_id" --format=JobID,JobName,Partition,MaxRSS,MaxVMSize,Elapsed,State
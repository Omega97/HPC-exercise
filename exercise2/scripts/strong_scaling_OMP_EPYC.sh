#!/bin/bash
#SBATCH --job-name=ex2EsOMP
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --output=output_epyc.%j.out
#SBATCH --error=error_epyc.%j.err
#SBATCH --time=00:45:00
#SBATCH --partition=EPYC
#SBATCH --nodelist=epyc003
#SBATCH --exclusive

# OpenMP strong scaling: fixed problem size, vary thread count.

cd "${SLURM_SUBMIT_DIR}" || exit 1

executable="../build/bin/mandelbrot"
output_dir="../results/"
output_file="${output_dir}strong_scaling_OMP_EPYC.csv"
number_workers=({1..64})
n=1000

mkdir -p "${output_dir}"
echo "Threads,Size,Walltime(s)" > "${output_file}"

export OMP_PLACES=cores
export OMP_PROC_BIND=close

for threads in "${number_workers[@]}"; do
  export OMP_NUM_THREADS="${threads}"
  result=$("${executable}" "${n}" "${n}" /dev/null)
  walltime=$(echo "$result" | awk '/Total Walltime/{print $4}')
  echo "${threads},${n},${walltime}" >> "${output_file}"
done

job_id=$SLURM_JOB_ID
echo "Job Statistics for Job ID $job_id:"
sacct -j "$job_id" --format=JobID,JobName,Partition,MaxRSS,MaxVMSize,Elapsed,State
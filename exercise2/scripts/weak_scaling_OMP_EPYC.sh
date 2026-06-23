#!/bin/bash
#SBATCH --job-name=ex2EwOMP
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --output=output_epyc.%j.out
#SBATCH --error=error_epyc.%j.err
#SBATCH --time=02:00:00
#SBATCH --partition=EPYC
#SBATCH --nodelist=epyc003
#SBATCH --exclusive

# OpenMP weak scaling: constant work per thread (C pixels).

cd "${SLURM_SUBMIT_DIR}" || exit 1

executable="../build/bin/mandelbrot"
output_dir="../results/"
output_file="${output_dir}weak_scaling_OMP_EPYC.csv"
lst1=(1 2 4 8)
lst2=({16..64..8})
number_workers=("${lst1[@]}" "${lst2[@]}")
C=1000000

mkdir -p "${output_dir}"
echo "Threads,Size,Walltime(s)" > "${output_file}"

export OMP_PLACES=threads
export OMP_PROC_BIND=close

for threads in "${number_workers[@]}"; do
  n=$(echo "sqrt($threads * $C)" | bc -l | xargs printf "%.0f")
  export OMP_NUM_THREADS="${threads}"
  result=$("${executable}" "${n}" "${n}" /dev/null)
  walltime=$(echo "$result" | awk '/Total Walltime/{print $4}')
  echo "${threads},${n},${walltime}" >> "${output_file}"
done

job_id=$SLURM_JOB_ID
echo "Job Statistics for Job ID $job_id:"
sacct -j "$job_id" --format=JobID,JobName,Partition,MaxRSS,MaxVMSize,Elapsed,State
#!/bin/bash
#SBATCH --job-name=ex1EPYCa24
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --output=../logs/output_epyc_alg24.%j.out
#SBATCH --error=../logs/error_epyc_alg24.%j.err
#SBATCH --time=02:00:00
#SBATCH --partition=EPYC
#SBATCH --exclusive

module load openMPI/4.1.6

output_dir="../results/"
output_file="${output_dir}barrierEPYC_alg24.csv"

barrier_algorithms=(2 4)
collective_operation="barrier"
number_processors=(2 4 8 16 32 48 64 96 128 176 224 256)

echo "Algorithm,Processors,Avg_Latency(us)" > ${output_file}

iterations=10

for iteration in $(seq 1 $iterations); do
  for barrier_algorithm in "${barrier_algorithms[@]}"; do
      for processors in "${number_processors[@]}"; do
        result=$(mpirun -np ${processors} \
          --map-by core \
          --mca coll_tuned_use_dynamic_rules true \
          --mca coll_tuned_${collective_operation}_algorithm ${barrier_algorithm} \
          ../bin/osu_${collective_operation} \
          -i 200 \
          -x 200)

        tail -n +4 <<< "$result" | awk "{print \"${barrier_algorithm},${processors},\" \$1}" >> ${output_file}
      done
  done
done
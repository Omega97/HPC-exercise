#!/bin/bash
# Pull ex2 scaling CSVs from Orfeo into the local repo (run from WSL on your laptop).
set -euo pipefail

# Uses the same key as the `orfeo` alias (~/.bashrc): orfeo_key_new
REMOTE="ocusmafait@195.14.102.215"
KEY="${HOME}/.ssh/orfeo_key_new"
REMOTE_DIR="~/HPC-exercise/exercise2/results"
LOCAL_DIR="/mnt/c/Users/monfalcone/PycharmProjects/HPC-exercise/exercise2/results"

mkdir -p "${LOCAL_DIR}"

if [[ ! -f "${KEY}" ]]; then
  echo "Missing SSH key: ${KEY}"
  echo "Your notes use orfeo_key_new. Check: ls -la ~/.ssh/orfeo_key*"
  exit 1
fi

scp -i "${KEY}" "${REMOTE}:${REMOTE_DIR}/strong_scaling_OMP_EPYC.csv" "${LOCAL_DIR}/"
scp -i "${KEY}" "${REMOTE}:${REMOTE_DIR}/weak_scaling_OMP_EPYC.csv" "${LOCAL_DIR}/"

echo "Synced to ${LOCAL_DIR}:"
ls -la "${LOCAL_DIR}"/*.csv
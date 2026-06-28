#!/bin/bash
# Render a square Mandelbrot view centered on a complex coordinate.
# Usage: ./render_spot.sh [half_span] [size] [I_max] [output.pgm]
#
# Default spot: 0.743643887037151 + 0.131825904205330i (Seahorse Valley)

set -euo pipefail

cd "$(dirname "$0")" || exit 1

CX=0.743643887037151
CY=0.131825904205330
HALF_SPAN="${1:-0.0015}"
SIZE="${2:-1200}"
I_MAX="${3:-4096}"
OUTPUT="${4:-../plots/mandelbrot_seahorse.pgm}"

XL=$(python3 -c "print(${CX} - ${HALF_SPAN})")
YL=$(python3 -c "print(${CY} - ${HALF_SPAN})")
XR=$(python3 -c "print(${CX} + ${HALF_SPAN})")
YR=$(python3 -c "print(${CY} + ${HALF_SPAN})")

EXEC="../build/bin/mandelbrot"
if [[ ! -x "${EXEC}" ]]; then
  bash make.sh -b
fi

mkdir -p "$(dirname "${OUTPUT}")"

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
export OMP_PLACES=cores
export OMP_PROC_BIND=close

echo "Center: ${CX} + ${CY}i"
echo "Half-span: ${HALF_SPAN} (width ${SIZE}, I_max=${I_MAX})"
echo "Region: [${XL}, ${XR}] x [${YL}, ${YR}]"

"${EXEC}" "${SIZE}" "${SIZE}" "${XL}" "${YL}" "${XR}" "${YR}" "${I_MAX}" "${OUTPUT}"
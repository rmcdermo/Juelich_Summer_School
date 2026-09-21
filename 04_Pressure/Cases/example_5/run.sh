#!/bin/bash
#
# Run one variant of Example 5 and file its output under results/.
#
#   ./run.sh [VARIANT]
#
# VARIANT is FFT (default), FFT_TP or UGLMAT -- the three input files in this
# directory. As in Example 4 the solver is not a line to comment
# in and out: each variant is its own input with its own CHID already set, so
# the three runs sit side by side in results/ instead of overwriting each other.
#
# Each input defines eight meshes through &MULT, so each run wants eight MPI
# ranks, one per mesh.
#
# This runs in the foreground with mpirun. On a cluster with a batch system use
# submit.sh instead, or it will run on the login node.
#
# Assumes fds and mpirun are already on PATH.

set -e

VARIANT="${1:-FFT}"
NP=8

cd "$(dirname "$0")"

INPUT="Example_5_${VARIANT}.fds"
if [ ! -f "$INPUT" ]; then
  echo "no such input: $INPUT" >&2
  echo "Variants are: FFT FFT_TP UGLMAT" >&2
  exit 1
fi

mkdir -p results
cp "$INPUT" results/

cd results
echo "running $INPUT on $NP process(es)"
mpirun -n "$NP" fds "$INPUT"

echo
echo "output in results/ as Example_5_${VARIANT}_*"
echo "plot it with:      python eval.py all"
echo "view it with:      cd results && smokeview Example_5_${VARIANT}"

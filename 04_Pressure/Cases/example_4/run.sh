#!/bin/bash
#
# Run one variant of Example 4 and file its output under results/.
#
#   ./run.sh [VARIANT]
#
# VARIANT is FFT (default), FFT_tight, ULMAT, UGLMAT_PARDISO or UGLMAT_HYPRE --
# the five input files in this directory. Unlike Example 3, the solver is not a
# line to comment in and out: each variant is its own input with its own CHID
# already set, because these are meant to be queued on a cluster rather than
# edited between runs.
#
# This runs in the foreground with mpirun. On a cluster with a batch system use
# submit.sh instead, or it will run on the login node.
#
# Assumes fds and mpirun are already on PATH.

set -e

VARIANT="${1:-FFT}"
NP=16          # each input defines 16 meshes through &MULT

cd "$(dirname "$0")"

INPUT="Example_4_${VARIANT}.fds"
if [ ! -f "$INPUT" ]; then
  echo "no such input: $INPUT" >&2
  echo "Variants are: FFT FFT_tight ULMAT UGLMAT_PARDISO UGLMAT_HYPRE" >&2
  exit 1
fi

mkdir -p results
cp "$INPUT" results/

cd results
echo "running $INPUT on $NP process(es)"
mpirun -n "$NP" fds "$INPUT"

echo
echo "output in results/ as Example_4_${VARIANT}_*"
echo "plot it with:      python eval.py all"

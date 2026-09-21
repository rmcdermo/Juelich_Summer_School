#!/bin/bash
#
# Run Example 3 and file its output under results/.
#
#   ./run.sh [VARIANT]
#
# VARIANT labels the run: FFT (default), ULMAT, FFT_tight, GLMAT or UGLMAT --
# the five &PRES lines on the slide.
# Switching solver is the point of the exercise, so it stays a hand edit in
# Example_3.fds -- this script does not touch the &PRES lines. It does check
# that the one you left uncommented is the variant you asked for, and stops if
# not: the variant becomes the CHID, so a mismatch would bake the wrong solver
# name into every output file, the .smv and the slices included.
#
# Assumes fds and mpirun are already on PATH.

set -e

VARIANT="${1:-FFT}"
INPUT=Example_3.fds
CHID=Example_3
NP=8          # Example_3.fds defines eight &MESH lines, so eight MPI processes

RUNID="${CHID}_${VARIANT}"

cd "$(dirname "$0")"

# Each &PRES line carries a "! VARIANT=name" tag; commented ones start with #,
# so this finds the single active line and the variant it stands for.
ACTIVE=$(sed -n "s/^[[:space:]]*&PRES.*![[:space:]]*VARIANT=\([A-Za-z0-9_]*\).*/\1/p" "$INPUT")
NACTIVE=$(printf '%s' "$ACTIVE" | grep -c . || true)

if [ "$NACTIVE" -ne 1 ]; then
  echo "Expected exactly one active &PRES line in $INPUT, found $NACTIVE." >&2
  echo "Leave one uncommented and put a # in front of the others." >&2
  exit 1
fi

if [ "$ACTIVE" != "$VARIANT" ]; then
  echo "The active &PRES line in $INPUT is $ACTIVE, but you asked for $VARIANT." >&2
  echo "Either edit $INPUT to uncomment the $VARIANT line, or run:" >&2
  echo "  ./run.sh $ACTIVE" >&2
  exit 1
fi

mkdir -p results

# Copy the input into results/ under the variant's name and set its CHID to
# match, so FDS names everything it writes -- .smv, slices, devc, .out -- after
# the variant. Nothing has to be renamed afterwards, the five runs coexist
# instead of overwriting each other's slices, and results/ ends up holding the
# input that produced each one. Running there also suits Smokeview, which needs
# the slice files in its working directory.
sed "s/CHID[[:space:]]*=[[:space:]]*'[^']*'/CHID='${RUNID}'/" "$INPUT" > "results/${RUNID}.fds"
if ! grep -q "CHID='${RUNID}'" "results/${RUNID}.fds"; then
  echo "could not set CHID in $INPUT -- is the &HEAD line still there?" >&2
  exit 1
fi

cd results
echo "running $INPUT as $RUNID on $NP process(es)"
mpirun -n "$NP" fds "${RUNID}.fds"

echo
echo "output in results/ as ${RUNID}_*"
echo "plot it with:      python eval.py"
echo "view it with:      cd results && smokeview ${RUNID}"

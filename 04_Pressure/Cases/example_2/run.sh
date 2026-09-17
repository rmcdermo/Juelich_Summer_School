#!/bin/bash
#
# Run Example 2 and file its output under results/.
#
#   ./run.sh
#
# Assumes fds and mpirun are already on PATH.

set -e

INPUT=Example_2.fds
CHID=Example_2
NP=1          # Example_2.fds defines one &MESH, so one MPI process

cd "$(dirname "$0")"
mkdir -p results

# Copy the input in and run there, so results/ holds the whole run: the input
# as it was when it ran, every file FDS writes, and the .smv pointing at all of
# them by plain name. That makes results/ something you can zip and send, and
# it is the directory Smokeview has to be started from anyway -- the .smv names
# its slice files without a path.
cp -f "$INPUT" results/
cd results
echo "running $INPUT on $NP process(es)"
mpirun -n "$NP" fds "$INPUT"

echo
echo "output in results/"
echo "plot it with:      python eval.py"
echo "view it with:      cd results && smokeview ${CHID}"
echo
echo "Bonus: set &MISC CCVOL_LINK to 0.2 or 0.9 in $INPUT and run again."
echo "Watch the time step count in ${CHID}.out and the mass balance from eval.py."

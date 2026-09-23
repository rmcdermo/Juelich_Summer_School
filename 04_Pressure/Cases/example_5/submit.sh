#!/bin/bash
#
# Queue all three variants of Example 5, one job each.
#
#   ./submit.sh
#
# A Slurm example -- adapt the directives to your own system. The three runs
# are independent, so they can sit in the queue at the same time; nothing here
# has to run in order.
#
# Each input defines eight meshes through &MULT, so each job wants eight MPI
# ranks, one per mesh. Give each rank its own core: two of the three figures
# are cost comparisons between solvers, and ranks sharing cores would show up
# in them as solver cost.
#
# Wall clock, 8 ranks, for the 30 s these runs cover. Two machines, because
# they disagree by more than you would guess -- an Apple M4 laptop and the
# spark Linux/Intel cluster, both under FDS 6.11.1. The figures are drawn from
# the spark set:
#
#                       M4 6.11.1     spark 6.11.1
#     FFT_TP               23 min          17 min
#     UGLMAT               52 min          60 min
#     FFT                 397 min         169 min
#
# The 16 h limit below is sized for FFT on the slower of the two with room to
# spare. Nothing here is hurt by a job finishing well inside its limit.

set -e
cd "$(dirname "$0")"
mkdir -p results

for VARIANT in FFT FFT_TP UGLMAT; do
  INPUT="Example_5_${VARIANT}.fds"
  cp "$INPUT" results/
  sbatch <<SLURM
#!/bin/bash
#SBATCH --job-name=E5_${VARIANT}
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=16:00:00
# --chdir below is already results/, so this is results/Example_5_<V>.log
#SBATCH --output=Example_5_${VARIANT}.log
#SBATCH --chdir=$(pwd)/results

export OMP_NUM_THREADS=1
mpirun -n 8 fds ${INPUT}
SLURM
  echo "queued ${VARIANT}"
done

echo
echo "when they finish, cut the one time step the error figure needs out of the"
echo "_pressit.csv files before copying anything back -- the plain FFT one runs"
echo "to about a gigabyte, 2000 iterations a half step for the whole run:"
echo
echo "  ./slice_pressit.sh 2462          (or: python eval.py slice --step 2462)"
echo
echo "then everything the figures need is, per variant:"
echo "  results/Example_5_<VARIANT>_devc.csv                iterations, error, cpu time"
echo "  results/Example_5_<VARIANT>_pressit_step2462.csv    the sliced time step"
echo "  results/Example_5_<VARIANT>.out                     the log, for the record"

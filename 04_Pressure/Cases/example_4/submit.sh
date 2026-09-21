#!/bin/bash
#
# Queue all five variants of Example 4, one job each.
#
#   ./submit.sh
#
# A Slurm example -- adapt the directives to your own system. The five runs are
# independent, so they can sit in the queue at the same time; nothing here has
# to run in order.
#
# Each input defines 16 meshes through &MULT, so each job wants 16 MPI ranks,
# one per mesh. Give each rank its own core: the third panel of the figure is a
# cost comparison between solvers, and ranks sharing cores would show up in it
# as solver cost.
#
# Wall clock on the reference cluster, 16 ranks, for the 20 s these runs cover:
#
#     FFT               2.2 h
#     UGLMAT_HYPRE      5.3 h
#     ULMAT             7.1 h
#     FFT_tight         7.5 h
#     UGLMAT_PARDISO   11.6 h
#
# The 24 h limit below is sized for the slowest of them with room to spare.
#
# Both UGLMAT runs carry MAX_PRESSURE_ITERATIONS=1. On this case that costs
# nothing -- they hold one iteration a half step and leave velocity error at
# 1.7e-15 -- but do not carry the setting over to a case with a long domain
# without checking it. Example 5 is the same cap in a 128 m tunnel, and there
# it goes numerically unstable.

set -e
cd "$(dirname "$0")"
mkdir -p results

for VARIANT in FFT FFT_tight ULMAT UGLMAT_PARDISO UGLMAT_HYPRE; do
  INPUT="Example_4_${VARIANT}.fds"
  cp "$INPUT" results/
  sbatch <<SLURM
#!/bin/bash
#SBATCH --job-name=E4_${VARIANT}
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
# --chdir below is already results/, so this is results/Example_4_<V>.log
#SBATCH --output=Example_4_${VARIANT}.log
#SBATCH --chdir=$(pwd)/results

export OMP_NUM_THREADS=1
srun -n 16 fds ${INPUT}
SLURM
  echo "queued ${VARIANT}"
done

echo
echo "when they finish, everything the figures need is:"
echo "  results/Example_4_<VARIANT>_devc.csv   iterations, velocity error, cpu time"
echo "  results/Example_4_<VARIANT>_line.csv   the radial velocity profiles"

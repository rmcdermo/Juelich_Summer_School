#!/bin/bash
#SBATCH -J Example_4_FFT
#SBATCH -e YOUR_PATH_TO_EXAMPLE_4/results/Example_4_FFT.err
#SBATCH -o YOUR_PATH_TO_EXAMPLE_4/results/Example_4_FFT.log
#SBATCH --partition=batch
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --nodes=1

export OMP_NUM_THREADS=1
source ~/FDS/FDS6/bin/FDS6VARS.sh
source ~/FDS/FDS6/bin/SMV6VARS.sh

cd YOUR_PATH_TO_EXAMPLE_4/results
echo
echo `date`
echo "    Input file: Example_4_FFT.fds"
echo "     Directory: `pwd`"
echo "          Host: `hostname`"
echo "----------------" >> YOUR_PATH_TO_EXAMPLE_4/results/Example_4_FFT.qlog
echo "started running at `date`" >> YOUR_PATH_TO_EXAMPLE_4/results/Example_4_FFT.qlog
mpirun -n 16 fds Example_4_FFT.fds 
echo "finished running at `date`" >> YOUR_PATH_TO_EXAMPLE_4/results/Example_4_FFT.qlog


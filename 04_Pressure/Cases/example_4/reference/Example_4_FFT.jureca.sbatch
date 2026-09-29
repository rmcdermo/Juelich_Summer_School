#!/bin/bash
#SBATCH -J Example_4_FFT

# budget account where contingent is taken from
#SBATCH --account=training2646

# chose JURECA partition, here the CPU part
#SBATCH --partition=dc-cpu

#SBATCH -e results/Example_4_FFT.err
#SBATCH -o results/Example_4_FFT.log
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --nodes=1

export OMP_NUM_THREADS=1

module use -a /p/project1/cias-7/modules_fire
module load Stages/2025
module load FDS/6.11.1

cd results
echo
echo `date`
echo "    Input file: Example_4_FFT.fds"
echo "     Directory: `pwd`"
echo "          Host: `hostname`"
echo "----------------" >> results/Example_4_FFT.qlog
echo "started running at `date`" >> results/Example_4_FFT.qlog
srun fds Example_4_FFT.fds 
echo "finished running at `date`" >> results/Example_4_FFT.qlog


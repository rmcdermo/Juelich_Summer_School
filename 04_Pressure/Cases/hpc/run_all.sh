export FDS=<Path_to_your_FDS_executable>

export OMP_NUM_THREADS=1
mpiexec -np 4 $FDS hpc_4mesh_4mpi_1omp.fds
mpiexec -np 2 $FDS hpc_4mesh_2mpi_1omp.fds

export OMP_NUM_THREADS=2
mpiexec -np 4 $FDS hpc_4mesh_4mpi_2omp.fds
mpiexec -np 2 $FDS hpc_4mesh_2mpi_2omp.fds

export OMP_NUM_THREADS=4
mpiexec -np 4 $FDS hpc_4mesh_4mpi_4omp.fds
mpiexec -np 2 $FDS hpc_4mesh_2mpi_4omp.fds

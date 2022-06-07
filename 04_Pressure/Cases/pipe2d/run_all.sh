export FDS=<Path_to_your_FDS_executable>

mpiexec -np 4 $FDS pipe2d_fft_default.fds
mpiexec -np 4 $FDS pipe2d_fft_tol-5.fds
mpiexec -np 4 $FDS pipe2d_uglmat.fds
mpiexec -np 4 $FDS pipe2d_ulmat.fds
mpiexec -np 4 $FDS pipe2d_ulmat_tol-5.fds
mpiexec -np 4 $FDS pipe2d_uscarc.fds
mpiexec -np 4 $FDS pipe2d_uscarc_insep.fds

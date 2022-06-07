export FDS=<Path_to_your_FDS_executable>

mpiexec -np 16 $FDS sandia_fft_default.fds
mpiexec -np 16 $FDS sandia_fft_tol-4.fds
mpiexec -np 16 $FDS sandia_glmat.fds
mpiexec -np 16 $FDS sandia_scarc.fds
mpiexec -np 16 $FDS sandia_scarc_insep.fds
mpiexec -np 16 $FDS sandia_ulmat.fds

export FDS=<Path_to_your_FDS_executable>

mpiexec -np 30 $FDS wu_bakar_fft_tol-3.fds
mpiexec -np 30 $FDS wu_bakar_fft_tol-6.fds
mpiexec -np 30 $FDS wu_bakar_glmat.fds
mpiexec -np 30 $FDS wu_bakar_scarc_insep.fds

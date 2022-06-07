export FDS=<Path_to_your_FDS_executable>

mpiexec -np 4 $FDS dancing_eddies_fft_default.fds
mpiexec -np 4 $FDS dancing_eddies_fft_default_tp.fds
mpiexec -np 4 $FDS dancing_eddies_fft_tol-5.fds
mpiexec -np 4 $FDS dancing_eddies_fft_tol-5_tp.fds
mpiexec -np 4 $FDS dancing_eddies_uglmat.fds
mpiexec -np 4 $FDS dancing_eddies_ulmat_default.fds
mpiexec -np 4 $FDS dancing_eddies_ulmat_tol-5.fds
mpiexec -np 4 $FDS dancing_eddies_uscarc.fds
mpiexec -np 4 $FDS dancing_eddies_uscarc_insep.fds

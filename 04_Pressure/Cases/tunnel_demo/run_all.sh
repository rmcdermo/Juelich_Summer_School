export FDS=<Path_to_your_FDS_executable>

mpiexec -np 8 $FDS tunnel_demo_fft_tol-3.fds
mpiexec -np 8 $FDS tunnel_demo_fft_tol-6.fds
mpiexec -np 8 $FDS tunnel_demo_fft_tol0.fds
mpiexec -np 8 $FDS tunnel_demo_fft_tol2.fds
mpiexec -np 8 $FDS tunnel_demo_glmat.fds
mpiexec -np 8 $FDS tunnel_demo_scarc_insep.fds
mpiexec -np 8 $FDS tunnel_demo_ulmat.fds

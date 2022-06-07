export FDS=<Path_to_your_FDS_executable>

mpiexec -np 8 $FDS duct_flow_fft_tol-3.fds
mpiexec -np 8 $FDS duct_flow_uglmat.fds
mpiexec -np 8 $FDS duct_flow_ulmat_tol-3.fds
mpiexec -np 8 $FDS duct_flow_uscarc.fds

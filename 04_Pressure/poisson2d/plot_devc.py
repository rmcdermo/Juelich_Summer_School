# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

plt.rcParams.update({'font.size':16})

# the directory 'prepared_results' contains the resutling 'chid_devc.csv' files for all cases from current directory
# the plots are saved in the directory 'plots' by default
# if you want to run the tests for your own and evauluate the plots based on your own results, then change results_dir to './'
#result_dir = './'
result_dir = 'prepared_results/'
geometry   = 'poisson2d_4mesh'
solvers    = ['fft_default','fft_tight','scarc_default','scarc_tight','uscarc','uglmat']

units = {}
quantities = {}
data = {}


# ----------------------------------------------------------------------------------------------
# Read in chid_devc.csv files for all solvers
# ----------------------------------------------------------------------------------------------
for solver in solvers:

   # get name of devices file for selected solver
   devc_solver = result_dir + geometry + '_' + solver + '_devc.csv'

   # open file, read in the first two lines containing the quantities and units, finally close the file again
   fin = open(devc_solver, 'r')
   units_line = fin.readline()
   quantities_line = fin.readline()
   fin.close()

   # split the two lines by comma to determie the column data, results are now lists
   units_solver = units_line.strip().split(',')
   quantities_solver = quantities_line.strip().split(',')

   # remove quotes and end-of-line characters
   for i in range(len(quantities_solver)):
       units_solver[i] = units_solver[i].strip().strip("\"")
       quantities_solver[i] = quantities_solver[i].strip().strip("\"")

   # read whole DEVC data
   data_solver = np.loadtxt(devc_solver, delimiter=',', skiprows=2)

   units[solver] = units_solver
   quantities[solver] = quantities_solver
   data[solver] = data_solver


# -----------------------------------------------------------------------------------------------
# Structure of data_solver:      
#        data_solver[:,0]  : time step
#        data_solver[:,i]  : selected quantity 'quantity[i]' with unit 'unit_solver[i] '
# -----------------------------------------------------------------------------------------------
# The following devices are available
#     i=1 : u-velocity
#     i=2 : w-velocity
#     i=3 : pressure
#     i=4 : maximum velocity error
#     i=5 : pressure iterations
#     i=6 : scarc iterations                  (only available for scarc and uscarc-solvers)
#     i=7 : scarc convergence rate            (only available for scarc and uscarc-solvers)
#     i=8 : scarc residual                    (only available for scarc and uscarc-solvers)
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# Plot comparison of pressure trace for FFT-default, FFT-tight and UGLMAT (i=3)
# -----------------------------------------------------------------------------------------------
index = 3
plt.plot(data['uglmat'][:, 0],      data['uglmat'][:, index],      'k-',  label= 'UGLMAT')
plt.plot(data['fft_default'][:, 0], data['fft_default'][:, index], 'b-',  label= 'FFT-default')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, index],   'r--', label= 'FFT-tight')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Pressure (Pa)")
plt.xlim(0.0, 0.5)
plt.ylim(-2.5, 3.0)
plt.legend(loc='lower left', fontsize=12)
plt.tick_params(labelsize=12)
plt.savefig("plots/pressure_traces_fft.png")
plt.clf()

# -----------------------------------------------------------------------------------------------
# Plot comparison of pressure trace for ScaRC, UScaRC and UGLMAT (i=3)
# -----------------------------------------------------------------------------------------------
index = 3
plt.plot(data['uglmat'][:, 0],        data['uglmat'][:, index],        'k-',  label= 'UGLMAT')
plt.plot(data['scarc_default'][:, 0], data['scarc_default'][:, index], 'r-.', label= 'ScaRC-default')
plt.plot(data['scarc_tight'][:, 0],   data['scarc_tight'][:, index],   'g--', label= 'ScaRC-tight')
plt.plot(data['uscarc'][:, 0],        data['uscarc'][:, index],        'b:',  label= 'UScaRC')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Pressure (Pa)")
plt.xlim(0.0, 0.5)
plt.ylim(-2.5, 3.0)
plt.legend(loc='lower left', fontsize=12)
plt.tick_params(labelsize=12)
plt.savefig("plots/pressure_traces_scarc.png")
plt.clf()

# -----------------------------------------------------------------------------------------------
# Plot comparison of maximum velocity error for FFT-default, FFT-tight and UGLMAT (i=4)
# -----------------------------------------------------------------------------------------------
index = 4
plt.semilogy(data['uglmat'][:, 0],      data['uglmat'][:, index],      'k-', label= 'UGLMAT')
plt.semilogy(data['fft_default'][:, 0], data['fft_default'][:, index], 'b-', label= 'FFT-default')
plt.semilogy(data['fft_tight'][:, 0],   data['fft_tight'][:, index],   'r-', label= 'FFT-tight')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Velocity error (m/s)")
plt.xlim(0.0, 0.5)
plt.legend(loc='center right', fontsize=12)
plt.tick_params(labelsize=10)
plt.savefig("plots/velocity_error_fft.png")
plt.clf()

# -----------------------------------------------------------------------------------------------
# Plot comparison of maximum velocity error for ScaRC-default, ScaRC-tight and UGLMAT (i=4)
# -----------------------------------------------------------------------------------------------
index = 4
plt.semilogy(data['uglmat'][:, 0],        data['uglmat'][:, index],        'k-', label= 'UGLMAT')
plt.semilogy(data['scarc_default'][:, 0], data['scarc_default'][:, index], 'b-', label= 'ScaRC-default')
plt.semilogy(data['scarc_tight'][:, 0],   data['scarc_tight'][:, index],   'r-', label= 'ScaRC-tight')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Velocity error (m/s)")
plt.xlim(0.0, 0.5)
plt.legend(loc='center right', fontsize=12)
plt.tick_params(labelsize=10)
plt.savefig("plots/velocity_error_scarc.png")
plt.clf()

# -----------------------------------------------------------------------------------------------
# Plot comparison of number of pressure iterations for FFT-default, FFT-tight and UGLMAT (i=5)
# -----------------------------------------------------------------------------------------------
index = 5
plt.plot(data['uglmat'][:, 0],      data['uglmat'][:, index],      'k-', label= 'UGLMAT')
plt.plot(data['fft_default'][:, 0], data['fft_default'][:, index], 'b-', label= 'FFT-default')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, index],   'r-', label= 'FFT-tight')

max_ite_default  = max(data['fft_default'][20:,index])
mean_ite_default = np.mean(data['fft_default'][20:,index])
max_ite_tight    = max(data['fft_tight'][20:,index])
mean_ite_tight   = np.mean(data['fft_tight'][20:,index])

print ("Max  number of pressure iterations for FFT-default  : {:8.1f}  ".format(max_ite_default))
print ("Mean number of pressure iterations for FFT-default  : {:8.1f}\n".format(mean_ite_default))
print ("Max  number of pressure iterations for FFT-tight    : {:8.1f}  ".format(max_ite_tight))
print ("Mean number of pressure iterations for FFT-tight    : {:8.1f}\n".format(mean_ite_tight))

plt.xlabel("Simulated Time [s]")
plt.ylabel("Pressure Iterations")
plt.xlim(0.0, 0.5)
plt.ylim(-10, max_ite_tight+2)
plt.tick_params(labelsize=12)
plt.legend(loc='upper left', fontsize=12)
plt.savefig("plots/pressure_iterations_fft.png")
plt.clf()

# -----------------------------------------------------------------------------------------------
# Plot comparison of number of pressure iterations for ScaRC-default, ScaRC-tight and UGLMAT (i=5)
# -----------------------------------------------------------------------------------------------
index = 5
plt.plot(data['uglmat'][:, 0],        data['uglmat'][:, index],        'k-',  label= 'UGLMAT')
plt.plot(data['scarc_default'][:, 0], data['scarc_default'][:, index], 'r--', label= 'ScaRC-default')
plt.plot(data['scarc_tight'][:, 0],   data['scarc_tight'][:, index],   'g-',  label= 'ScaRC-tight')
plt.plot(data['uscarc'][:, 0],        data['uscarc'][:, index],        'b:',  label= 'UScaRC')

max_ite_default  = max(data['scarc_default'][20:,index])
mean_ite_default = np.mean(data['scarc_default'][20:,index])
max_ite_tight  = max(data['scarc_tight'][20:,index])
mean_ite_tight = np.mean(data['scarc_tight'][20:,index])

print ("Max  number of pressure iterations for ScaRC-default: {:8.1f}  ".format(max_ite_default))
print ("Mean number of pressure iterations for ScaRC-default: {:8.1f}\n".format(mean_ite_default))
print ("Max  number of pressure iterations for ScaRC-tight  : {:8.1f}  ".format(max_ite_tight))
print ("Mean number of pressure iterations for ScaRC-tight  : {:8.1f}\n".format(mean_ite_tight))

plt.xlabel("Simulated Time [s]")
plt.ylabel("Pressure Iterations")
plt.xlim(0.0, 0.5)
plt.ylim(-0.2, max_ite_tight+1)
plt.tick_params(labelsize=12)
plt.legend(loc='lower center',fontsize=12)
plt.savefig("plots/pressure_iterations_scarc.png")



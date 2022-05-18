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
geometry   = 'duct_flow'
solvers    =  ['fft_tight','scarc_tight', 'uscarc', 'uglmat']

units = {}
quantities = {}
data = {}

tend = 60.0

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
#     i=1 : volume flow in
#     i=2 : volume flow out
#     i=3 : maximum velocity error
#     i=4 : pressure iterations 
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# Plot comparison of pressure trace for FFT-default, FFT-tight and UGLMAT (i=3)
# -----------------------------------------------------------------------------------------------
plt.plot(data['uglmat'][:, 0],      data['uglmat'][:, 1],      'k-',  label= 'Ideal flow')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, 1],   'm--', label= 'FFT-tight - flow in')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, 2],   'g-',  label= 'FFT-tight - flow out')
plt.plot(data['uscarc'][:, 0],      data['uscarc'][:, 1],      'b-.', label= 'UScaRC - flow in')
plt.plot(data['uscarc'][:, 0],      data['uscarc'][:, 2],      'r:',  label= 'UScaRC - flow out')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Volume flow")
plt.xlim(0.0, tend)
#plt.ylim(-0.05, 0.07)
plt.legend(loc='lower left', fontsize=12)
plt.tick_params(labelsize=8)
plt.savefig("plots/volume_flow_fft_vs_uscarc.png")
plt.clf()


# -----------------------------------------------------------------------------------------------
# Plot comparison of pressure trace for FFT-default, FFT-tight and UGLMAT (i=3)
# -----------------------------------------------------------------------------------------------
plt.plot(data['uglmat'][:, 0],      data['uglmat'][:, 1],      'k-',  label= 'Ideal flow')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, 1],   'm--', label= 'FFT-tight - flow in')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, 2],   'g-',  label= 'FFT-tight - flow out')
plt.plot(data['scarc_tight'][:, 0], data['scarc_tight'][:, 1], 'b-.', label= 'ScaRC-tight - flow in')
plt.plot(data['scarc_tight'][:, 0], data['scarc_tight'][:, 2], 'r-',  label= 'ScaRC-tight - flow out')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Volume flow")
plt.xlim(0.0, tend)
#plt.ylim(-0.05, 0.07)
plt.legend(loc='lower left', fontsize=12)
plt.tick_params(labelsize=8)
plt.savefig("plots/volume_flow_with_fft_vs_scarc.png")
plt.clf()


# -----------------------------------------------------------------------------------------------
# Plot comparison of maximum velocity error for FFT-default, FFT-tight and UGLMAT (i=4)
# -----------------------------------------------------------------------------------------------
index = 3
plt.semilogy(data['uglmat'][:, 0],    data['uglmat'][:, index],    'k-', label= 'UGLMAT')
plt.semilogy(data['fft_tight'][:, 0], data['fft_tight'][:, index], 'g-', label= 'FFT-tight')
plt.semilogy(data['uscarc'][:, 0],    data['uscarc'][:, index],    'r-', label= 'UScaRC')

plt.xlabel("Simulated Time [s]")
plt.ylabel("Velocity error (m/s)")
plt.xlim(0.1, tend)
plt.legend(loc='center left', fontsize=12)
plt.tick_params(labelsize=10)
plt.savefig("plots/velocity_error.png")
plt.clf()


# -----------------------------------------------------------------------------------------------
# Plot comparison of number of pressure iterations for FFT-default, FFT-tight and UGLMAT (i=5)
# -----------------------------------------------------------------------------------------------
index = 4
plt.plot(data['uglmat'][:, 0],      data['uglmat'][:, index],      'k-', label= 'UGLMAT')
plt.plot(data['fft_tight'][:, 0],   data['fft_tight'][:, index],   'g-', label= 'FFT-tight')
plt.plot(data['uscarc'][:, 0],      data['uscarc'][:, index],      'r:', label= 'UScaRC')

max_ite_tight    = max(data['fft_tight'][50:,4])
mean_ite_tight   = np.mean(data['fft_tight'][50:,4])

print ("Max  number of pressure iterations for FFT-tight  : {:8.1f}  ".format(max_ite_tight))
print ("Mean number of pressure iterations for FFT-tight  : {:8.1f}\n".format(mean_ite_tight))

plt.xlabel("Simulated Time [s]")
plt.ylabel("Pressure Iterations")
plt.xlim(0.0, tend)
plt.ylim(-2, max_ite_tight+2)
plt.tick_params(labelsize=12)
plt.legend(loc='upper left', fontsize=12)
plt.savefig("plots/pressure_iterations.png")
plt.clf()


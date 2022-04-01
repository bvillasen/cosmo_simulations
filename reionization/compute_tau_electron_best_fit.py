import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
import scipy.integrate as integrals
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from constants_cosmo import Mpc

proj_dir = data_dir + 'projects/thermal_history/'
input_dir = proj_dir + 'data/ionization_history/'
output_dir = proj_dir + 'data/ionization_history/'
create_directory( output_dir )

sigma_thompson = 6.652458e-29 #m^2
c = 299792458 #m/s

H0 = 67.66 * 1e3 / Mpc
Omega_L = 0.6889
Omega_M = 0.3111


tau_all = []

z_integral = np.linspace( 0, 14, 100 )

for model_id in range(16):
  file_name = input_dir + f'solution_{model_id}.h5'
  print ( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' )

  z = file['z'][...]
  ne = file['n_e'][...] * 1e6 #m^-3
  file.close()

  current_a = 1 / ( z + 1 )
  H = H0 * np.sqrt( Omega_M/current_a**3 + Omega_L )
  tau = ne * sigma_thompson / ( 1 + z ) * c / H

  tau_integral = []
  for zval in z_integral:
    indices = z <= zval
    tau_reion = integrals.simps( tau[indices][::-1], z[indices][::-1] )
    tau_integral.append( tau_reion )
  tau_integral = np.array( tau_integral )
  tau_all.append( tau_integral )

tau_all = np.array( tau_all ).T
tau_min, tau_max = [], []
for tau_vals in tau_all:
  tau_min.append( tau_vals.min() )
  tau_max.append( tau_vals.max() )
tau_max = np.array( tau_max ).T
tau_min = np.array( tau_min ).T
tau_range = { 'max':tau_max, 'min':tau_min }


file_name = input_dir + f'solution_HL.h5'
print ( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r' )

z = file['z'][...]
ne = file['n_e'][...] * 1e6 #m^-3
file.close()

current_a = 1 / ( z + 1 )
H = H0 * np.sqrt( Omega_M/current_a**3 + Omega_L )
tau = ne * sigma_thompson / ( 1 + z ) * c / H

tau_integral = []
for zval in z_integral:
  indices = z <= zval
  tau_reion = integrals.simps( tau[indices][::-1], z[indices][::-1] )
  tau_integral.append( tau_reion )
tau_integral = np.array( tau_integral )

tau_electron_best_fit = { 'HL':tau_integral, 'high':tau_max, 'low':tau_min   }

file_name = output_dir + 'tau_electron_best_fit.pkl'
Write_Pickle_Directory( tau_electron_best_fit, file_name )

# 
# 
# file_name = output_dir + 'tau_range.pkl'
# Write_Pickle_Directory( tau_range, file_name )
# 
# file_name = input_dir + f'solution_HL.h5'
# # file_name = input_dir + f'solution_modified_Gamma_sigmoid.h5'
# print ( f'Loading File: {file_name}' )
# file = h5.File( file_name, 'r' )
# 
# z = file['z'][...]
# ne = file['n_e'][...] * 1e6 #m^-3
# file.close()
# 
# current_a = 1 / ( z + 1 )
# H = H0 * np.sqrt( Omega_M/current_a**3 + Omega_L )
# tau = ne * sigma_thompson / ( 1 + z ) * c / H
# 
# tau_integral = []
# for zval in z_integral:
#   indices = z <= zval
#   tau_reion = integrals.simps( tau[indices][::-1], z[indices][::-1] )
#   tau_integral.append( tau_reion )
# tau_integral = np.array( tau_integral )
# 
# tau_HL = { 'HL':tau_integral }
# 
# # file_name = output_dir + 'tau_HL.pkl'
# file_name = output_dir + 'tau_modified_Gamma_sigmoid.pkl'
# Write_Pickle_Directory( tau_HL, file_name )

import os, sys
import numpy as np
import pickle
import pymc
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from load_tabulated_data import load_data_boera 

ps_data_dir = base_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( data_boera_dir )
z_vals_boera = data_boera['z_vals'] 


output_dir = root_dir + 'data_simulated/'
create_directory( output_dir )

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )

params_to_select = { 'wdm_mass': 4.0, 'scale_H_ion':1.0, 'scale_H_Eheat':0.9, 'deltaZ_H':0.0 }
selected_sims = SG.Select_Simulations( params_to_select, tolerance=5e-3 )
print( f'Selected simulations: {selected_sims}' )

# Load analysis data for the selected simulation
SG.Load_Grid_Analysis_Data( sim_ids=selected_sims, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=None, load_thermal=False )

# Get the flux power spectrum from the selected simulation
sim_id = selected_sims[0]
power_spectrum_data = SG.Grid[sim_id]['analysis']['power_spectrum']
sim_z_vals = power_spectrum_data['z']

# Select the power spectrum at certain redshifts
z_vals = [ 5.0, 4.6, 4.2 ]
ps_indices = Select_Indices( z_vals, sim_z_vals, tolerance=1e-3 )
ps_indices_boera = Select_Indices( z_vals, z_vals_boera, tolerance=1e-3)
 
kmin, kmax = None, None
# Generate the data from the simulation
sigma_fraction = 0.01
sim_data = {}
for data_id, ps_indx in enumerate(ps_indices):
  z = power_spectrum_data['z'][ps_indx]
  k_vals  = power_spectrum_data['k_vals'][ps_indx]
  ps_mean = power_spectrum_data['ps_mean'][ps_indx]
  if kmin is None: kmin = 0.9*k_vals.min()
  if kmax is None: kmax = 1.1*k_vals.max()
  k_indices = ( k_vals >= kmin ) * ( k_vals <= kmax )
  k_vals  = k_vals[k_indices]
  ps_mean = ps_mean[k_indices]
  
  # Interpolate at the k_vals from Boera
  indx_boera = ps_indices_boera[data_id]
  ps_data_boera = data_boera[indx_boera]
  z_boera = ps_data_boera['z'] 
  k_boera = ps_data_boera['k_vals']
  ps_boera = ps_data_boera['power_spectrum']
  ps_sigma_boera = ps_data_boera['power_spectrum_error']
  cov_matrix_boera = ps_data_boera['covariance_matrix'] 
  # print( ps_sigma_boera / ps_boera )
  if np.abs( z_boera - z ) > 1e-2:
    print( 'ERROR Redshift difference between boera data: ')
  ps_interp = np.interp(k_boera, k_vals, ps_mean )
  k_vals = k_boera
  ps_mean = ps_interp
  
  # ps_sigma = ps_mean * sigma_fraction
  ps_sigma = ps_sigma_boera * sigma_fraction
  delta_power = ps_mean * k_vals / np.pi
  delta_power_error = ps_sigma * k_vals / np.pi
  cov_matrix = cov_matrix_boera * sigma_fraction**2
  sim_data[data_id] = { 'z':z, 'k_vals':k_vals, 'power_spectrum':ps_mean, 'power_spectrum_error':ps_sigma, 'delta_power':delta_power, 'delta_power_error':delta_power_error, 'covariance_matrix':cov_matrix }

sim_data['z_vals'] = np.array([ sim_data[id]['z'] for id in sim_data ])


# file_name = output_dir + f'simulated_power_spectrum_sigma{sigma_fraction}.pkl'
# file_name = output_dir + f'simulated_power_spectrum_covmatrix{sigma_fraction}.pkl'
file_name = output_dir + f'simulated_power_spectrum_sigmaBoera{sigma_fraction}.pkl'
Write_Pickle_Directory( sim_data, file_name )





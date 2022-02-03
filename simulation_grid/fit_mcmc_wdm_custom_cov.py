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
from mcmc_data_functions import Get_Comparable_Composite, Get_Comparable_Composite_from_Grid, Write_MCMC_Results
from plot_mcmc_functions import Plot_Comparable_Data, Plot_MCMC_Stats
from mcmc_sampling_functions import get_mcmc_model
from plot_mcmc_corner import Plot_Corner

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1
  

# Directories 
ps_data_dir = base_dir + '/lya_statistics/data/'

# Fields to Fit using the mcmc
fields_to_fit = 'P(k)+'
data_ps_sets = [ 'Boera' ]
# data_ps_sets = [ 'BoeraC' ]

# error_type = 'sigma'
error_type = 'covmatrix'

independent_redshift = False
use_inv_wdm = True

fit_name = ''
data_label  = ''
for data_set in data_ps_sets:
  fit_name += data_set + '_'
  data_label += data_set + ' + '
fit_name = fit_name[:-1] 
data_label = data_label[:-3]

fit_name += f'_{error_type}'

print(f'Data Label: {data_label} {fit_name}')

# extra_label = 'sigmaResCosmo_'
extra_label = None
if extra_label is not None: fit_name += f'_{extra_label}'


mcmc_dir = root_dir + 'fit_mcmc/'
if rank == 0: create_directory( mcmc_dir )
output_dir = mcmc_dir + f'fit_results_{fields_to_fit}_{fit_name}/'
if rank == 0: create_directory( output_dir, )
if independent_redshift: 
  z_indx = rank
  output_dir += f'fit_redshift/'
  if rank == 0: create_directory( output_dir )
  output_dir += f'redshift_{z_indx}/'
  if use_mpi: comm.Barrier()
  create_directory( output_dir )

load_covariance_matrix = False
if error_type == 'covmatrix': load_covariance_matrix = True 

# Apply the resolution correction to the P(k) fronm the simulations
# FPS_correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc_delta.pkl'
# FPS_resolution_correction = Load_Pickle_Directory( correction_file_name ) 
FPS_resolution_correction = None #Instead we apply a systematic uncertanty to the observed P(k)

# Change wdm_mass to inv_wdm_mass
if use_inv_wdm: Grid_Parameters = Invert_wdm_masses( Grid_Parameters )

#Load custom power spectrum measurement
custom_ps_data = { 'root_dir': root_dir + 'flux_power_spectrum', 'file_base_name':'flux_ps_resample_boera_native', 'stats_base_name':'statistics_resample_boera_native' }
custom_data = { 'P(k)': custom_ps_data } 

# sim_ids = [0]
sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=FPS_resolution_correction, custom_data=custom_data )

kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )
sim_ids = SG.sim_ids

#Define the redshift range for the fit 
z_min, z_max = 4.2, 5.0

if independent_redshift:
  z_vals = [ 4.2, 4.6, 5.0 ]
  z_val = z_vals[z_indx]
  z_min = z_val - 0.05
  z_max = z_val + 0.05

# Use P(k) instead of Delta_P(k)
no_use_delta_p = True 

data_systematic_uncertainties = None
ps_parameters = { 'range':ps_range, 'data_dir':ps_data_dir, 'data_sets':data_ps_sets  }
comparable_data = Get_Comparable_Composite( fields_to_fit, z_min, z_max, ps_parameters=ps_parameters, log_ps=False, systematic_uncertainties=data_systematic_uncertainties, no_use_delta_p=no_use_delta_p, load_covariance_matrix=load_covariance_matrix   )
comparable_grid = Get_Comparable_Composite_from_Grid( fields_to_fit, comparable_data, SG, log_ps=False, no_use_delta_p=no_use_delta_p )
Plot_Comparable_Data( fields_to_fit, comparable_data, comparable_grid, output_dir, log_ps=False  )

params = SG.parameters
stats_file   = output_dir + 'fit_mcmc.pkl'
samples_file = output_dir + 'samples_mcmc.pkl'

nIter = 5000000 
nBurn = nIter // 10
nThin = 1
model, params_mcmc = get_mcmc_model( comparable_data, comparable_grid, fields_to_fit, 'mean', SG, error_type=error_type )
MDL = pymc.MCMC( model )  
MDL.sample( iter=nIter, burn=nBurn, thin=nThin )
stats = MDL.stats()
param_stats = {}
for p_id in params.keys():
  p_name = params[p_id]['name']
  p_stats = stats[p_name]
  params[p_id]['mean'] = p_stats['mean']
  params[p_id]['sigma'] = p_stats['standard deviation']
Plot_MCMC_Stats( stats, MDL, params_mcmc,  stats_file, output_dir, plot_corner=False, plot_model=False )
param_samples = Write_MCMC_Results( stats, MDL, params_mcmc,  stats_file, samples_file,  output_dir  )


data_labels = [ '' ]
corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
                  'wdm_mass':r'$m_{\mathrm{WDM}}$  [keV]', 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]'       }
Plot_Corner( param_samples, data_labels, corner_labels, output_dir,n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=False  )  


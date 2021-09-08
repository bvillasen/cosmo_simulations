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
from mcmc_sampling_functions import mcmc_model_4D
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

z_reion = 6.3
z_reion_data = { 'z':z_reion, 'sigma':0.025 }

# Directories 
ps_data_dir = base_dir + '/lya_statistics/data/'

# Fields to Fit using the mcmc
# fields_to_fit = 'P(k)+tau_HeII'
# data_ps_sets = [ 'Boss', 'Irsic', 'Boera', 'Walther' ]
fields_to_fit = 'P(k)+z_ion_H'
data_ps_sets = [ 'Boera' ]

fit_name = ''
data_label  = ''
for data_set in data_ps_sets:
  fit_name += data_set + '_'
  data_label += data_set + ' + '
fit_name = fit_name[:-1] 
data_label = data_label[:-3]
fit_name += f'_zreion{z_reion}' 
print(f'Data Label: {data_label}')

mcmc_dir = root_dir + 'fit_mcmc/'
base_dir = mcmc_dir + f'fit_results_{fields_to_fit}_{fit_name}/'
if rank==0: create_directory( mcmc_dir )
if rank==0: create_directory( base_dir )
base_dir += 'fit_redshift/' 
if rank==0: create_directory( base_dir )

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data(  load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', load_thermal=True )

# kmax = 0.1
kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )
sim_ids = SG.sim_ids

# z_vals = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0 ] 
z_vals = [  4.2, 4.6, 5.0 ] 

# z_indx = 0 
z_indx = rank
output_dir = base_dir + f'redshift_{z_indx}/'
create_directory( output_dir )



z_val = z_vals[z_indx]

z_min = z_val - 0.05
z_max = z_val + 0.05  
ps_parameters = { 'range':ps_range, 'data_dir':ps_data_dir, 'data_sets':data_ps_sets  }
comparable_data = Get_Comparable_Composite( fields_to_fit, z_min, z_max, ps_parameters=ps_parameters, log_ps=False, z_reion=z_reion_data  )
comparable_grid = Get_Comparable_Composite_from_Grid( fields_to_fit, comparable_data, SG, log_ps=False )
Plot_Comparable_Data( fields_to_fit, comparable_data, comparable_grid, output_dir, log_ps=False  )

params = SG.parameters


stats_file   = output_dir + 'fit_mcmc.pkl'
samples_file = output_dir + 'samples_mcmc.pkl'

nIter = 500000 
nBurn = nIter / 5
nThin = 1
model, params_mcmc = mcmc_model_4D( comparable_data, comparable_grid, fields_to_fit, 'mean', SG )
MDL = pymc.MCMC( model )  
MDL.sample( iter=nIter, burn=nBurn, thin=nThin )
stats = MDL.stats()
param_stats = {}
for p_id in params.keys():
  p_name = params[p_id]['name']
  p_stats = stats[p_name]
  params[p_id]['mean'] = p_stats['mean']
  params[p_id]['sigma'] = p_stats['standard deviation']
Plot_MCMC_Stats( stats, MDL, params_mcmc,  stats_file, output_dir, plot_corner=False )
param_samples = Write_MCMC_Results( stats, MDL, params_mcmc,  stats_file, samples_file,  output_dir  )


data_labels = [ '' ]
corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$'      }
Plot_Corner( param_samples, data_labels, corner_labels, output_dir,n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=False  )  


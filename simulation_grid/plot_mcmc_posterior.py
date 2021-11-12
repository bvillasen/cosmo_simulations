import os, sys
import numpy as np
import pickle
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
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



independent_redshift = False

data_name = 'fit_results_P(k)+_Boera_'
# data_name = 'fit_results_P(k)+_BoeraC_'


if independent_redshift: 
  z_indx = rank
  data_name += f'/fit_redshift/redshift_{z_indx}'
mcmc_dir = root_dir + 'fit_mcmc/'
input_dir = mcmc_dir + f'{data_name}/' 
output_dir = input_dir 
create_directory( output_dir )


  
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
params = SG.parameters


stats_file = input_dir + 'fit_mcmc.pkl'
samples_file = input_dir + 'samples_mcmc.pkl'
print( f'Loading File: {stats_file}')
stats = pickle.load( open( stats_file, 'rb' ) )
for p_id in params.keys():
  p_name = params[p_id]['name']
  p_stats = stats[p_name]
  params[p_id]['mean'] = p_stats['mean']
  params[p_id]['sigma'] = p_stats['standard deviation']
print( f'Loading File: {samples_file}')
param_samples = pickle.load( open( samples_file, 'rb' ) )

bins = {}
bins[0] = { 'min':min(params[0]['values']), 'max':max(params[0]['values']), 'n':30 }
bins[1] = None
bins[2] = None

data_labels =  '' 
corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
                  'wdm_mass':r'$m_{\mathrm{WDM}}$  [keV]'      }
Plot_Corner( param_samples, data_labels, corner_labels, output_dir, bins=bins, n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=False  )  




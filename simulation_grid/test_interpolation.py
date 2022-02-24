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
from interpolation_functions import Interpolate_multi_dimensional_from_grid
from mcmc_data_functions import Get_Comparable_Composite, Get_Comparable_Composite_from_Grid
from plot_mcmc_functions import Plot_Comparable_Data

# Directories 
ps_data_dir = base_dir + '/lya_statistics/data/'
output_dir = data_dir + 'figures/interpolation_test/'
create_directory( output_dir )

# Fields to interpolate
fields_to_fit = 'P(k)+'
data_ps_sets = [ 'Boera' ]

#Load custom power spectrum measurement
custom_ps_data = { 'root_dir': root_dir + 'flux_power_spectrum', 'file_base_name':'flux_ps_sampled_boera_extended', 'stats_base_name':None }
custom_data = { 'P(k)': custom_ps_data } 

sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=None, custom_data=custom_data )
grid_params = SG.parameters
print( grid_params)

kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )

#Define the redshift range for the fit 
z_min, z_max = 4.2, 5.0

# Use P(k) instead of Delta_P(k)
no_use_delta_p = True 

data_systematic_uncertainties = None
load_covariance_matrix = False
ps_parameters = { 'range':ps_range, 'data_dir':ps_data_dir, 'data_sets':data_ps_sets  }
comparable_data = Get_Comparable_Composite( fields_to_fit, z_min, z_max, ps_parameters=ps_parameters, log_ps=False, systematic_uncertainties=data_systematic_uncertainties, no_use_delta_p=no_use_delta_p, load_covariance_matrix=load_covariance_matrix   )
comparable_grid = Get_Comparable_Composite_from_Grid( fields_to_fit, comparable_data, SG, log_ps=False, no_use_delta_p=no_use_delta_p )
Plot_Comparable_Data( fields_to_fit, comparable_data, comparable_grid, output_dir, log_ps=False  )


param_vals = [7.0, 0.6, 0.1, 0.0]

interpolation = Interpolate_multi_dimensional_from_grid( param_vals, comparable_grid, fields_to_fit, 'mean', SG ) 
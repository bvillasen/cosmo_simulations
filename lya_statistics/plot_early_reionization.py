import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from simulation_grid_functions import Get_Grid_Params, Select_Simulations
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from plot_thermal_history import Plot_T0_gamma_evolution

root_dir   = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/reduced_files/'
output_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/early_reionization/'
create_directory( output_dir )

deltaZ_H = 0.2

z_reion = 6 + deltaZ_H

grid_sim_params, sim_dirs = Get_Grid_Params( root_dir )
params_to_select = { 'scale_He':None, 'deltaZ_He':None, 'scale_H':None, 'deltaZ_H':deltaZ_H }
selected_sims = Select_Simulations( params_to_select, grid_params=grid_sim_params )
n_selected = len( selected_sims )
print( f'N selected simulations: {n_selected}' )

n_files = 56
data_all = {}
for sim_id in selected_sims:
  sim_dir = sim_dirs[sim_id]
  sim_data = {}
  T0_vals = []
  for n_file in range(n_files):
    file_name = sim_dir + f'/analysis_files/{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    ps_data = file['lya_statistics']['power_spectrum']
    k  = ps_data['k_vals'][...] 
    ps = ps_data['p(k)'][...]
    indx = ps > 0
    snap_data = {  'z':z, 'k_vals': k[indx], 'ps_mean':ps[indx] }
    sim_data[n_file] = snap_data
    file_name = sim_dir + f'/analysis_files/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    data = Load_Pickle_Directory( file_name )
    T0 = 10**(data['T0']['mean'])
    T0_vals.append( T0 )
  sim_data['z_vals'] = np.array([ sim_data[i]['z'] for i in sim_data ])
  sim_data['T0'] = np.array(T0_vals)
  sim_data['z'] = sim_data['z_vals']
  data_all[sim_id] = sim_data


# Sort to color the liunes:
z_color = 5.0
ps_max_vals = []
for data_id in data_all:
  data_sim = data_all[data_id]
  z_vals = data_sim['z_vals']
  diff = np.abs( z_vals - z_color )
  diff_min = diff.min()
  if diff_min > 1e-3: print( f'WARNING: redshift difference: {diff_min}' )
  indx = np.where( diff == diff_min )[0][0]
  data_snap = data_sim[indx]
  ps_vals = data_snap['ps_mean']
  ps_max = ps_vals.max() 
  ps_max_vals.append(ps_max)
  
ps_max_vals = np.array( ps_max_vals )
sim_ids = np.array( selected_sims )
indices_sorted = np.argsort( ps_max_vals )
sim_ids_sorted = sim_ids[indices_sorted]

n_lines = len( data_all )
colormap = matplotlib.cm.get_cmap('turbo')
colors = colormap( np.linspace(0,1,n_lines) )

for sim_id in data_all:
  indx = np.where( sim_ids_sorted == sim_id)[0][0]
  data_all[sim_id]['line_color'] = colors[indx]


Plot_Power_Spectrum_Grid( output_dir, ps_data=data_all, fig_name=f'ps_grid_z{z_reion}.png', scales='small_reduced', line_colors=None, sim_data_sets=None, linewidth=0.6, line_alpha=0.5, line_color='C0', c_boera='k' )

Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name=f'T0_evolution_grid_z{z_reion}', interpolate_lines=True, plot_gamma=False  )

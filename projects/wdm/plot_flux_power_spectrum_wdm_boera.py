import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from colors import * 
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid

ps_data_dir = cosmo_dir + 'lya_statistics/data/'

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir ) 

colors = [ 'C0', 'C1', 'C2', 'C3', 'C4']
labels = [ r'$m_\mathrm{WDM}=0.5 \, \mathrm{keV}$', r'$m_\mathrm{WDM}=1.0 \, \mathrm{keV}$', r'$m_\mathrm{WDM}=2.0 \, \mathrm{keV}$', r'$m_\mathrm{WDM}=3.0 \, \mathrm{keV}$', r'CDM']

L_Mpc = 50
base_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/'

snapshots = [ 25, 29, 33 ]

factors = [ 1., 1., 1. ]
ps_samples = {}
sim_names = [ 'wdm_m0.5kev', 'wdm_m1.0kev', 'wdm_m2.0kev', 'wdm_m3.0kev', 'cdm'   ]
for sim_id, sim_name in enumerate(sim_names):
  ps_samples[sim_id] = {}
  input_dir = base_dir + f'1024_{L_Mpc}Mpc_{sim_name}/analysis_files/'
  for snap_id, n_snap in enumerate(snapshots):
    file_name = input_dir + f'{n_snap}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    k  = file['lya_statistics']['power_spectrum']['k_vals'][...]
    pk = file['lya_statistics']['power_spectrum']['p(k)'][...] 
    indices = pk > 0
    pk = pk[indices]
    k  = k[indices]
    factor = factors[snap_id]
    pk = pk * k / np.pi * factor
    ps_samples[sim_id][snap_id] = { 'z':z, 'k_vals':k, 'Highest_Likelihood':pk }
  ps_samples[sim_id]['z_vals'] = np.array([ ps_samples[sim_id][i]['z'] for i in ps_samples[sim_id]   ])
  ps_samples[sim_id]['line_color'] = colors[sim_id]
  ps_samples[sim_id]['label'] = labels[sim_id]
  
  

# Apply resolution correction
correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
FPS_correction = Load_Pickle_Directory( correction_file_name ) 
corr_z_vals = FPS_correction['z_vals']


n_snapshots = 3
for sim_id in ps_samples:
  for z_id in range(n_snapshots):
    ps_data = ps_samples[sim_id][z_id]
    z = ps_data['z']
    k_vals = ps_data['k_vals']
    ps_mean = ps_data['Highest_Likelihood']
    # ps_h = ps_data['higher']
    # ps_l = ps_data['lower']
    z_diff = np.abs( corr_z_vals - z )
    if z_diff.min() > 5e-2: 
      print( f'Large redshift diference: {z_diff.min()}')
      continue  
    z_indx = np.where( z_diff == z_diff.min() )[0]
    if len( z_indx ) != 1 :
      print( f'ERROR: Unable to match the redshift of the correction fator. {z} -> {correction_z_vals[z_indx]}  ')
      exit(-1)
    z_indx = z_indx[0]
    correction = FPS_correction[z_indx]
    correction_k_vals = correction['k_vals']
    correction_ps_factor = correction['delta_factor']
    indices = correction_ps_factor > 1
    new =  correction_ps_factor[indices] - 1
    correction_ps_factor[indices] = 1 + new * 1
    k_diff = np.abs( k_vals - correction_k_vals )
    # print( f'{z} {correction_ps_factor}')
    if k_diff.sum() > 1e-6:
       print(f'ERROR: Large k difference for FPS correction: {k_diff.sum()}.')
       exit(-1)
    ps_mean = ps_mean / correction_ps_factor
    # ps_h = ps_h / correction_ps_factor
    # ps_l = ps_l / correction_ps_factor
    k_l = 0.08
    indices = k_vals >= k_l
    n = indices.sum()
    factor = np.linspace( 1, 1.2, n)
    print(factor)
    ps_mean[indices] *= factor
    ps_samples[sim_id][z_id]['Highest_Likelihood'] = ps_mean 
    
  
Plot_Power_Spectrum_Grid( output_dir, sim_data_sets=None, ps_samples=ps_samples,  fig_name='flux_ps_wdm_boera.png', scales='small_highz', line_colors=None,  )


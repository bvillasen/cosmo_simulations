import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from constants_cosmo import Mpc, kpc
from tools import *
from cosmology import Cosmology
from load_data import Load_Skewers_File, load_analysis_data
from calculus_functions import *
from stats_functions import compute_distribution
from data_optical_depth import data_optical_depth_Bosman_2021
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum
from figure_functions import *

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'

# Box parameters
Lbox = 25000.0 #kpc/h
N = 1024
dx = Lbox / N
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list  = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'HI_density', 'los_velocity', 'temperature' ]


sim_name = '1024_25Mpc_cdm'
sim_dir = base_dir + sim_name + '/'
input_dir  = sim_dir + 'skewers_files/'

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/vel_peculiar/'
create_directory( output_dir )

snap_ids =  [ 25, 29, 33 ]
# for snap_id in snap_ids:
snap_id = 33

n_skewers = 1 
  
# for space in [ 'real', 'redshift']:
space = 'real'
space = 'redshift'

skewer_dataset = Load_Skewers_File( snap_id, input_dir, axis_list=axis_list, fields_to_load=field_list )
cosmology = {}
cosmology['H0'] = skewer_dataset['H0']
cosmology['Omega_M'] = skewer_dataset['Omega_M']
cosmology['Omega_L'] = skewer_dataset['Omega_L']
cosmology['current_z'] = skewer_dataset['current_z']
skewers_data = { field:skewer_dataset[field][:n_skewers] for field in field_list }

current_z = cosmology['current_z']
current_a = 1 / ( current_z + 1 )

cosmo = Cosmology()
H = cosmo.get_Hubble( current_a ) / 1e3 # km / s / kpc


dr = dx * current_a / cosmo.h
r_proper = (np.linspace( 0, N-1, N) + 0.5 ) * dr
vel_Hubble = H * r_proper   #km/s

vel_peculiar = skewer_dataset['los_velocity'][0] # km/s


kpc_km = kpc / 1e3
dr_km = dr * kpc_km
H_seg = H / kpc_km
grad_vpec = np.zeros_like( vel_peculiar )
grad_vpec[1:-1] = ( vel_peculiar[2:] - vel_peculiar[:-2] ) / ( 2 * dr_km )
grad_vpec[0]    = ( vel_peculiar[1]  - vel_peculiar[0]  ) / (  dr_km )
grad_vpec[-1]   = ( vel_peculiar[-1] - vel_peculiar[-2]  ) / ( dr_km )



method_list = [ 'error_function', 'gaussian', ''] 

data_Flux_gradvel = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box, space=space, method='gaussian_pecvel_grad'  )
data_Flux_gauss = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box, space=space, method='gaussian'  )
data_Flux_err = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box, space=space, method='error_function'  )

tau_gradvel = data_Flux_gradvel['skewers_tau'][0]
tau_gauss = data_Flux_gauss['skewers_tau'][0]
tau_err = data_Flux_err['skewers_tau'][0]

flux_gradvel = np.exp( - tau_gradvel ) 
flux_gauss   = np.exp( - tau_gauss ) 
flux_eff     = np.exp( - tau_err ) 

# 
# out_file_name = output_dir + f'lya_flux_{space}_{snap_id:03}.h5'
# file = h5.File( out_file_name, 'w' )
# file.attrs['current_z'] = skewer_dataset['current_z']
# file.attrs['Flux_mean'] = data_Flux_cdm['Flux_mean']
# file.create_dataset( 'vel_Hubble', data=data_Flux_cdm['vel_Hubble'] )
# file.create_dataset( 'skewers_Flux', data=data_Flux_cdm['skewers_Flux'] )
# file.close()
# print( f'Saved File: {out_file_name}')
# 



figure_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 16
legend_font_size = 12
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1.5
text_color = 'k'

nrows, ncols = 5, 1

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,3*nrows))
plt.subplots_adjust( hspace = 0.05, wspace=0.2 )

ax = ax_l[0]
ax.plot( vel_Hubble, vel_peculiar )
ax.axhline( y=0, ls='--', c='C3' )
ax.set_xlim( vel_Hubble.min(), vel_Hubble.max() )
ax.set_xticklabels([])
ax.set_ylabel( r'$v_\mathrm{pec} \,\, \mathregular{[km \, s^{-1}]}$', fontsize=label_size)
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


ax = ax_l[1]
factor = 1e-16
ax.plot( vel_Hubble, grad_vpec/factor )
ax.axhline( y=H_seg/factor, ls='--', c='C2', label= r'$H \,\, \mathregular{[10^{-16} \, s^{-1}]}$' )
ax.axhline( y=0, ls='--', c='C3' )
ax.set_xlim( vel_Hubble.min(), vel_Hubble.max() )
ax.set_xticklabels([])
ax.set_ylabel( r'$ \nabla v_\mathrm{pec} \,\, \mathregular{[10^{-16} \, s^{-1}]}$', fontsize=label_size)
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.legend( frameon=False, fontsize=legend_font_size)

ax = ax_l[2]
ax.plot( vel_Hubble, tau_gauss, label='original' )
ax.plot( vel_Hubble, tau_gradvel,  ls='--', label='grad pec vel' )
ax.set_xlim( vel_Hubble.min(), vel_Hubble.max() )
ax.set_xticklabels([])
ax.set_ylabel( r'$\tau$', fontsize=label_size)
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.set_yscale('log')
ax.legend( frameon=False, fontsize=legend_font_size)


ax = ax_l[3]
ax.plot( vel_Hubble, flux_gauss, label='original' )
ax.plot( vel_Hubble, flux_gradvel, ls='--', label='grad pec vel' )
ax.set_xlim( vel_Hubble.min(), vel_Hubble.max() )
ax.set_ylabel( r'$F$', fontsize=label_size)
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.legend( frameon=False, fontsize=legend_font_size)
ax.set_xticklabels([])
ax.set_ylim( 0, 1 )

ax = ax_l[4]
ax.plot( vel_Hubble, (flux_gradvel / flux_gauss - 1) / 1e-11, label='original / grad pec vel' )
ax.set_xlim( vel_Hubble.min(), vel_Hubble.max() )
ax.set_ylabel( r'$\Delta F / F \,\, \times 10^{-11}$ ', fontsize=label_size)
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.legend( frameon=False, fontsize=legend_font_size)
delta = 3
ax.set_ylim( -delta, delta )


ax = ax_l[-1]
ax.set_xlabel( r'$v_\mathrm{H} \,\, \mathregular{[km \, s^{-1}]}$  ', fontsize=label_size)


figure_name = output_dir + f'skewer_flux_{snap_id}_new.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )




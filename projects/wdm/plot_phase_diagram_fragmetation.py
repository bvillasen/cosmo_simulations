import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
from mpl_toolkits.axes_grid1 import ImageGrid
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from figure_functions import *
from data_optical_depth import *
from colors import *
from load_data import load_analysis_data
from cosmology import Cosmology
from constants_cosmo import Mpc, Myear, Gcosmo, Msun, kpc
from internal_energy import get_temperature

sim_dir = input_dir = data_dir + 'cosmo_sims/1024_25Mpc_fragmentation/cdm/'
output_dir = sim_dir + 'figures/phase_diagram/'
create_directory( output_dir )

n_file = 29
# for n_file in range( 56):

phase_diagram = {}
data_id = 0
input_dir = sim_dir + '/analysis_files/'
data = load_analysis_data( n_file, input_dir, phase_diagram=True, lya_statistics=False, )
current_z = data['cosmology']['current_z']
pd_data = data['phase_diagram']
phase = pd_data['data']
n_dens = pd_data['n_dens']
n_temp = pd_data['n_temp']
temp_max = pd_data['temp_max']
temp_min = pd_data['temp_min']
dens_max = pd_data['dens_max']
dens_min = pd_data['dens_min']
log_temp_max = np.log10(temp_max)
log_temp_min = np.log10(temp_min) 
log_dens_max = np.log10(dens_max)
log_dens_min = np.log10(dens_min) 
log_temp_vals = np.linspace( log_temp_min, log_temp_max, n_temp )
log_dens_vals = np.linspace( log_dens_min, log_dens_max, n_dens )
dens_points, temp_points = np.meshgrid( log_dens_vals, log_temp_vals )
temp_points = temp_points.flatten()
dens_points = dens_points.flatten()
phase_1D = phase.flatten() 
indices = np.where(phase_1D > 0 )
phase_1D = phase_1D[indices]
dens_points = dens_points[indices]
temp_points = temp_points[indices]
indices = np.where( phase_1D > 1*phase_1D.min() )
phase_1D = phase_1D[indices]
dens_points = dens_points[indices]
temp_points = temp_points[indices]
phase_1D = np.log10( phase_1D )
phase_diagram[data_id] = { 'dens_points':dens_points, 'temp_points':temp_points, 'phase_1D':phase_1D, 'z':current_z}





current_a = 1 / ( current_z + 1 )
cosmo = Cosmology(z_start=100)

Lbox = 25000 #kpc/h 
n_points = 1024
Lbox *= current_a / cosmo.h 
dx = Lbox / n_points

rho_mean = cosmo.rho_gas_mean / Msun * (kpc*100)**3 / current_a**3 # Msun / kpc^3

n_samples = 100
delta_range = np.logspace( -3, 5, n_samples )  
density = rho_mean * delta_range

gamma = 5/3
p_truelove =  16 / ( gamma / np.pi ) * Gcosmo * ( density * dx ) * ( density * dx );
U_truelove = p_truelove / ( gamma - 1 )
u_truelove = U_truelove / density
temp_truelove = get_temperature( u_truelove )





fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1

text_color = 'black'


import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


n_rows = 1
n_cols = 1


data_all = phase_diagram

colormap =  'turbo'
alpha = 0.6

x_min, x_max = -3, 5
y_min, y_max =  0, 7.

fig, ax = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width*n_cols,6*n_rows))
plt.subplots_adjust( hspace = 0.1, wspace=0.2)

sim_id = 0
z = phase_diagram[sim_id]['z'] 
dens_points = phase_diagram[sim_id]['dens_points']
temp_points = phase_diagram[sim_id]['temp_points']
phase_1D    = phase_diagram[sim_id]['phase_1D'] 

im = ax.scatter( dens_points, temp_points, c=phase_1D, s=0.1,   alpha=alpha, cmap=colormap  )
# im = ax.imshow( phase_1D, vmin=-1, vmax=1,  alpha=alpha, cmap=colormap, extent=(dens_points.min(), dens_points.max(), temp_points.min(), temp_points.max()), origin='lower'  )

ax.plot( np.log10(delta_range), np.log10(temp_truelove), '--', c='k' )

cb = plt.colorbar(im,   )
cb.ax.tick_params(labelsize=tick_label_size_major, size=tick_size_major, color=text_color, width=tick_width_major, length=tick_size_major, labelcolor=text_color, direction='in' )
[sp.set_linewidth(border_width) for sp in cb.ax.spines.values()]
# cb.set_label( r'$\log_{10}  \,\, P\,(\Delta, T\,) $', fontsize=label_size )
# 
ax.set_aspect( 1.2)
# 
font = {'fontname': 'Helvetica',
    'color':  text_color,
    'weight': 'normal',
    'size': label_size,
    'ha':'center'
    }
# cb.set_label( r'$\log_{10}  \,\, P\,(\Delta, T\,) $', fontdict=font )
ax.set_ylabel(r'$\log_{10} \, T \,\,[\,\mathrm{K}\,]$', fontsize=label_size , color=text_color)
ax.set_xlabel(r'$\log_{10} \, \Delta$ ', fontsize=label_size , color=text_color )

text  = r'$z = {0:.1f}$'.format( z ) 
ax.text(0.03, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)

# text  = f'{labels[sim_id]}' 
# ax.text(0.95, 0.95, text, horizontalalignment='right',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)

ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in')
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
[sp.set_linewidth(border_width) for sp in ax.spines.values()]
ax.set_xlim( x_min, x_max )
ax.set_ylim( y_min, y_max )


out_fileName = output_dir + f'phase_diagram_{n_file}.png'
fig.savefig( out_fileName,  pad_inches=0.1,  facecolor=fig.get_facecolor(),  bbox_inches='tight', dpi=300)
print( f'Saved Image:  {out_fileName} ')


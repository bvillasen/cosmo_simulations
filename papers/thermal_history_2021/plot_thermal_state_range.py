import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib
import pylab
import pickle
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from data_thermal_history import *
from colors import *
from interpolation_functions import interp_line_cubic
from figure_functions import *
 
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
input_dir = root_dir + 'properties/'
output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir ) 

data_sets = Load_Pickle_Directory( input_dir+'T0_grid.pkl' )
z = data_sets[0]['z']
n = len(z)
temp_max, temp_min = [], []
for z_id in range(n):
  vmax, vmin = -np.inf, np.inf
  for data_id in data_sets:
    data_set = data_sets[data_id]
    temp = data_set['T0'][z_id]
    vmax = max( vmax, temp )
    vmin = min( vmin, temp )
  temp_max.append( vmax )
  temp_min.append( vmin )

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
data_name = data_boss_irsic_boera
print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# Obtain distribution of all the fields
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )
samples_T0 = samples_fields['T0']

data_T0 = { 'z': samples_T0['z'], 'T0':samples_T0['Highest_Likelihood'], 'high':samples_T0['higher'], 'low':samples_T0['lower'] }
data_to_plot = { 0: data_T0 }
data_to_plot[0]['label'] = 'This Work'
data_to_plot[0]['color'] = 'k'





text_color  = 'black'


ymin, ymax = 0.6, 1.8
xmin, xmax = 1.95, 9.0
nrows = 1
ncols = 1

figure_width = 8

color_data_0 = orange
color_data_1 = 'C3'

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 12, 12
tick_width_major, tick_width_minor = 1.5, 1

border_width = 1.5

font_size = 16
legend_font_size = 12
alpha = 0.5


interpolate_lines = True
n_samples_interp = 1000
# 
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)



n_lines = len( data_sets )
print( f'n_lines: {n_lines}' )

# colormap = colormap = palettable.cmocean.sequential.Algae_20_r.mpl_colormap
# colormap = palettable.colorbrewer.sequential.YlGnBu_9_r.mpl_colormap
# colormap = palettable.scientific.sequential.Nuuk_20_r.mpl_colormap
colormap = palettable.scientific.sequential.LaPaz_20.mpl_colormap
colors = colormap( np.linspace(0,1,n_lines) )

color_range = colors[0]
color_range = ocean_blue
color_range = sky_blue
color_range = light_orange


alpha = 0.3
temp_all = [ ]
for data_id in data_sets:
  # if data_id >335 and data_id < 3340: continue
  if data_id == 335: continue
  if data_id == 338: continue
  data_set = data_sets[data_id]
  if 'label' in data_set: label = data_set['label']
  else: label = ''
  z = data_set['z']
  T0 = data_set['T0'] / 1e4
  z0 = z.copy()
  color = light_orange
  color = 'C1'
  if interpolate_lines:
    z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
    T0 = interp_line_cubic( z, z_interp, T0 )
    z = z_interp
  label = ''
  temp_all.append( T0)
  ax.plot( z, T0, c=color,  label=label, alpha=0.3, lw=1, zorder = 2)

n_lines = len( temp_all )
z = z_interp
n = len(z)
temp_max, temp_min = [], []
for z_id in range(n):
  vmax, vmin = -np.inf, np.inf
  for data_id in range(n_lines):
    temp = temp_all[data_id][z_id]
    vmax = max( vmax, temp )
    vmin = min( vmin, temp )
  temp_max.append( vmax )
  temp_min.append( vmin )
  
temp_max = np.array(temp_max)
temp_min = np.array(temp_min)  

z_max, z_min = 3.70, 2.85
indices = (z <= z_max) * ( z>=z_min )
z_vals = z[indices]
temp_vals = temp_max[indices]
t0 = temp_vals[0]
t1 = temp_vals[-1]
temp = (t0 - t1) / ( z_max-z_min) * ( z_vals-z_min) + t1
temp_max[indices] = temp
 
z_max, z_min = 6.32, 5.6
indices = (z <= z_max) * ( z>=z_min )
z_vals = z[indices]
temp_vals = temp_max[indices]
t0 = temp_vals[0]
t1 = temp_vals[-1]
temp = (t0 - t1) / ( z_max-z_min) * ( z_vals-z_min) + t1
temp_max[indices] = temp


ax.plot( [0,0], [1,1], c=color, label="Simulation Grid", alpha=0.8, lw=1 )

ax.fill_between( z, temp_max, temp_min, color=color_range, alpha=0.4, zorder=1 )

# data_sets = data_to_plot
# plot_interval = True
# for data_id in data_sets:
#   data_set = data_sets[data_id]
#   if 'label' in data_set: label = data_set['label']
#   else: label = ''
#   z = data_set['z']
#   T0 = data_set['T0'] / 1e4
#   z0 = z.copy()
#   color = 'k'
#   if interpolate_lines:
#     z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
#     T0 = interp_line_cubic( z, z_interp, T0 )
#     z = z_interp
#   if data_id == 0: label = 'This Work (Best-Fit)'
#   else: label = ''
#   ax.plot( z, T0, c=color, zorder=3, label=label, alpha=1, lw=1 )
#   if plot_interval:
#     high = data_set['high'] / 1e4
#     low  = data_set['low'] / 1e4
#     high[12] *= 1.005
#     low[12] *= 0.995
#     high[14] *= 0.995
#     low[14] *= 1.005
#     low[13] *= 1.002
#     if interpolate_lines:
#       high = interp_line_cubic( z0, z_interp, high )
#       low  = interp_line_cubic( z0, z_interp, low )
#     ax.fill_between( z, high, low, alpha=0.5, zorder=3, color=color )  





ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
# ax.set_ylabel( r'$T_0$  [$\mathregular{10^4}$ K]', fontsize=font_size, color=text_color  )
ax.set_ylabel( r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
# ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
ax.set_xlim( xmin, xmax )
ax.set_ylim( ymin, ymax)
leg = ax.legend(loc=1, frameon=False, fontsize=12,  )
for text in leg.get_texts():
  plt.setp(text, color = text_color)
[sp.set_linewidth(border_width) for sp in ax.spines.values()]



figure_name = output_dir + 'T0_grid'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


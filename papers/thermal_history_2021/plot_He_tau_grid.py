import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from colors import *
from tools import *
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019
from interpolation_functions import smooth_line
from interpolation_functions import interp_line


input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/properties/'
output_dir = data_dir + f'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir )


data_all = Load_Pickle_Directory( input_dir+'tau_HeII_grid.pkl')

z = data_all[0]['z']

n = len(z)
tau_min, tau_max = [], []
for i in range(n):
  vmax, vmin = -np.inf, np.inf
  for data_id in data_all:
    val = data_all[data_id]['tau'][i]
    vmax = max( vmax, val )
    vmin = min( vmin, val )
  tau_max.append( vmax )
  tau_min.append( vmin )

input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic/'
file_name = input_dir + f'observable_samples/samples_fields.pkl'
fields_sim_data = Load_Pickle_Directory( file_name )



import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"



label_size = 11
legend_font_size = 7.5
fig_label_size = 15


tick_label_size_major = 10
tick_label_size_minor = 10
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.3
tick_width_minor = 1

color_data_tau = light_orange
sim_color = 'k'

color_range = sky_blue

if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
if system == 'Tornado': 
  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
  prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)


colormap = palettable.scientific.sequential.LaPaz_20.mpl_colormap
n_lines = len( data_all )
colors = colormap( np.linspace(0,1,n_lines) )

colors = plt.cm.cividis(np.linspace(0,1,n_lines))

ncols, nrows = 1, 1 
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,4*nrows))

interpolate_lines = True
n_samples_interp = 500

color_lines = dark_blue

tau_max, tau_min = np.ones(n_samples_interp), np.ones(n_samples_interp)
tau_max *= -np.inf
tau_min *=  np.inf
for data_id in data_all:
  data = data_all[data_id]
  z = data['z']
  tau = data['tau']
  if interpolate_lines:
    z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
    tau = interp_line( z, z_interp, tau, kind='quadratic' )
    z = z_interp
    for i in range( n_samples_interp ):
      tau_max[i] = max( tau_max[i], tau[i] )
      tau_min[i] = min( tau_min[i], tau[i] )
  ax.plot( z, tau, c=color_lines, lw=0.2, alpha=0.8, zorder=0 )
# 
label = 'Simulation Grid' 
lines = ax.plot( [0,1], [0,0], c=color_lines, lw=1, alpha=0.6, zorder=1, label=label )

label = ''
ax.fill_between( z, tau_min, tau_max, color=color_range,  alpha=0.4, zorder=1, label=label )



data_set = data_tau_HeII_Worserc_2019
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
tau_p = data_set['tau_sigma_p']
tau_m = data_set['tau_sigma_m']
tau_error = [ data_tau - tau_m , tau_p - data_tau  ]
points = ax.errorbar( data_z, data_tau, yerr=tau_error, fmt='o', color=color_data_tau, label=data_name, zorder=4)


lower_lims = [  [3.16, 5.2] ]
x_lenght = 0.025/4
for lower_lim in lower_lims:
  lim_x, lim_y = lower_lim
  ax.plot( [lim_x-x_lenght, lim_x+x_lenght], [lim_y, lim_y], color=color_data_tau,  zorder=4  )
  dx, dy = 0, 1
  ax.arrow( lim_x, lim_y, dx, dy,  color=color_data_tau, head_width=0.01, head_length=0.08,  zorder=4   )

z_vals = fields_sim_data['tau_HeII']['z']
tau = fields_sim_data['tau_HeII']['Highest_Likelihood']
tau_h = fields_sim_data['tau_HeII']['higher'] 
tau_l = fields_sim_data['tau_HeII']['lower'] 
if interpolate_lines:
  z_interp = np.linspace( z_vals[0], z_vals[-1], n_samples_interp ) 
  kind = 'cubic'
  tau   = interp_line( z_vals, z_interp, tau,   kind=kind )
  tau_h = interp_line( z_vals, z_interp, tau_h, kind=kind )
  tau_l = interp_line( z_vals, z_interp, tau_l, kind=kind )
  z_vals = z_interp
l1 = ax.plot( z_vals, tau, color=sim_color, zorder=3, label='This Work (Best-Fit)' )
ax.fill_between( z_vals, tau_h, tau_l, color=sim_color, alpha=0.6, zorder=3 )  

ax.set_xlim(2.0, 3.4 )
ax.set_ylim(0.3, 7 )

ax.set_xlabel( r'Redshift  $z$', fontsize=label_size )
ax.set_ylabel( r'HeII $\tau_{\mathrm{eff}}$', fontsize=label_size )

ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
# ax.set_xticks([ 2.2, 2.4, 2.6, 2.8, 3.0])

handles, labels = plt.gca().get_legend_handles_labels()
order = [0,1, 2]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], frameon=False, prop=prop)
# ax.legend( loc=2, frameon=False, prop=prop)

figure_name = output_dir + 'tau_He_grid_new.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


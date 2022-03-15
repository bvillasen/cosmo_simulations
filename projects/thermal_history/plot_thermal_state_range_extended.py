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
output_dir = data_dir + 'figures/thermal_history/paper/'
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
    
data_sets_ion = Load_Pickle_Directory( input_dir+'grid_ionization_fraction.pkl' )

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
data_name = data_boss_irsic_boera
print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# # Obtain distribution of all the fields
# file_name = input_dir + 'samples_fields.pkl'
# samples_fields = Load_Pickle_Directory( file_name )
# samples_T0 = samples_fields['T0']

# data_T0 = { 'z': samples_T0['z'], 'T0':samples_T0['Highest_Likelihood'], 'high':samples_T0['higher'], 'low':samples_T0['lower'] }
# data_to_plot = { 0: data_T0 }
# data_to_plot[0]['label'] = 'This Work'
# data_to_plot[0]['color'] = 'k'





text_color  = 'black'


nrows = 2
ncols = 2

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
# matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.12, wspace=0.13)



n_lines = len( data_sets )
print( f'n_lines: {n_lines}' )

# colormap = colormap = palettable.cmocean.sequential.Algae_20_r.mpl_colormap
# colormap = palettable.colorbrewer.sequential.YlGnBu_9_r.mpl_colormap
# colormap = palettable.scientific.sequential.Nuuk_20_r.mpl_colormap
colormap = palettable.scientific.sequential.LaPaz_20.mpl_colormap
colors = colormap( np.linspace(0,1,n_lines) )


for i in range(2):
  for j in range(2):
    ax = ax_l[i][j]
    
    if i == 0 and j==0:
      color = 'C1'
      temp_all = [ ]
      alpha_lines = 0.4
      alpha_range = 0.3
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
        if interpolate_lines:
          z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
          T0 = interp_line_cubic( z, z_interp, T0 )
          z = z_interp
        label = ''
        temp_all.append( T0)
        ax.plot( z, T0, c=color,  label=label, alpha=alpha_lines, lw=1, zorder = 2)

      ax.plot( [0,0], [1,1], c=color, label="Simulation Grid", alpha=0.8, lw=1 )
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
      ax.fill_between( z, temp_max, temp_min, color=color, alpha=alpha_range, zorder=1 )
      ax.set_ylabel( r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$', fontsize=font_size, color=text_color  )
      ymin, ymax = 0.6, 1.8
      xmin, xmax = 2.0, 9.0
      ax.set_xlim( xmin, xmax )
      ax.set_ylim( ymin, ymax)
      leg = ax.legend(loc=1, frameon=False, fontsize=12,  )


    if i == 0 and j==1:
      color = ocean_green
      alpha_lines = 0.4
      alpha_range = 0.3
      gamma_all = [ ]
      for data_id in data_sets:
          # if data_id == 335: continue
        # if data_id == 338: continue
        data_set = data_sets[data_id]
        if 'label' in data_set: label = data_set['label']
        else: label = ''
        z = data_set['z']
        gamma = data_set['gamma'] + 1 
        z0 = z.copy()
        if interpolate_lines:
          z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
          gamma = interp_line_cubic( z, z_interp, gamma )
          z = z_interp
        label = ''
        # z_max, z_min = 6.5, 5.5
        # indices = (z <= z_max) * ( z>=z_min )
        # selected_gamma = gamma[indices]
        # gamma_min = 0.94
        # selected_gamma[selected_gamma<gamma_min] = gamma_min 
        # gamma[indices] = selected_gamma
        gamma_all.append( gamma)
        ax.plot( z, gamma, c=color,  label=label, alpha=alpha_lines, lw=1, zorder = 2)

      ax.plot( [0,0], [1,1], c=color, label="Simulation Grid", alpha=0.8, lw=1 )
      n_lines = len( temp_all )
      z = z_interp
      n = len(z)
      gamma_max, gamma_min = [], []
      for z_id in range(n):
        vmax, vmin = -np.inf, np.inf
        for data_id in range(n_lines):
          gamma = gamma_all[data_id][z_id]
          vmax = max( vmax, gamma )
          vmin = min( vmin, gamma )
        gamma_max.append( vmax )
        gamma_min.append( vmin )
      
      gamma_max = np.array(gamma_max)
      gamma_min = np.array(gamma_min)  
      
      ax.fill_between( z, gamma_max, gamma_min, color=color, alpha=alpha_range, zorder=1 )
      ax.set_ylabel( r'$\gamma$', fontsize=font_size, color=text_color  )
      ax.set_xlim( 2, 7 )
      ax.set_ylim( 0.85, 1.6)
      leg = ax.legend(loc=1, frameon=False, fontsize=12,  )


    if i == 1 and j==0:
      # color = 'rebeccapurple'
      color = 'slateblue'
      alpha_lines = 0.4
      alpha_range = 0.3
      x_HI_all = [ ]
      for data_id in data_sets_ion:
          # if data_id == 335: continue
        # if data_id == 338: continue
        data_set = data_sets_ion[data_id]
        if 'label' in data_set: label = data_set['label']
        else: label = ''
        z = data_set['z']
        x_HI = data_set['x_HI'] 
        z0 = z.copy()
        # if interpolate_lines:
        #   z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
        #   x_HI = interp_line_cubic( z, z_interp, x_HI )
        #   z = z_interp
        label = ''
        x_HI_all.append( x_HI)
        ax.plot( z, x_HI, c=color,  label=label, alpha=alpha_lines, lw=1, zorder = 2)

      ax.plot( [0,0], [10,10], c=color, label="Simulation Grid", alpha=0.8, lw=1 )
      n_lines = len( temp_all )
      n = len(z)
      x_HI_max, x_HI_min = [], []
      for z_id in range(n):
        vmax, vmin = -np.inf, np.inf
        for data_id in range(n_lines):
          x_HI = x_HI_all[data_id][z_id]
          vmax = max( vmax, x_HI )
          vmin = min( vmin, x_HI )
        x_HI_max.append( vmax )
        x_HI_min.append( vmin )
      
      x_HI_max = np.array(x_HI_max)
      x_HI_min = np.array(x_HI_min)  
      
      ax.fill_between( z, x_HI_max, x_HI_min, color=color, alpha=alpha_range, zorder=1 )
      ax.set_ylabel( r'$x_\mathrm{HI}$', fontsize=font_size, color=text_color  )
      ax.set_xlim( 5, 12 )
      ax.set_ylim( -0.05, 1.05)
      leg = ax.legend(loc=4, frameon=False, fontsize=12,  )



    if i == 1 and j==1:
      color = sky_blue
      alpha_lines = 0.4
      alpha_range = 0.3
      x_HeII_all = [ ]
      for data_id in data_sets_ion:
          # if data_id == 335: continue
        # if data_id == 338: continue
        data_set = data_sets_ion[data_id]
        if 'label' in data_set: label = data_set['label']
        else: label = ''
        z = data_set['z']
        x_HeII = data_set['x_HeII'] 
        z0 = z.copy()
        # if interpolate_lines:
        #   z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
        #   x_HeII = interp_line_cubic( z, z_interp, x_HeII )
        #   z = z_interp
        label = ''
        x_HeII_all.append( x_HeII)
        ax.plot( z, x_HeII, c=color,  label=label, alpha=alpha_lines, lw=1, zorder = 2)

      ax.plot( [0,0], [10,10], c=color, label="Simulation Grid", alpha=0.8, lw=1 )
      n_lines = len( temp_all )
      n = len(z)
      x_HeII_max, x_HeII_min = [], []
      for z_id in range(n):
        vmax, vmin = -np.inf, np.inf
        for data_id in range(n_lines):
          x_HeII = x_HeII_all[data_id][z_id]
          vmax = max( vmax, x_HeII )
          vmin = min( vmin, x_HeII )
        x_HeII_max.append( vmax )
        x_HeII_min.append( vmin )
      
      x_HeII_max = np.array(x_HeII_max)
      x_HeII_min = np.array(x_HeII_min)  
      
      ax.fill_between( z, x_HeII_max, x_HeII_min, color=color, alpha=alpha_range, zorder=1 )
      ax.set_ylabel( r'$x_\mathrm{HeII}$', fontsize=font_size, color=text_color  )
      ax.set_xlim( 2, 5 )
      ax.set_ylim( -0.05, 1.05)
      leg = ax.legend(loc=4, frameon=False, fontsize=12,  )



    ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
    ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
    # ax.set_ylabel( r'$T_0$  [$\mathregular{10^4}$ K]', fontsize=font_size, color=text_color  )
    ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
    # ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
    for text in leg.get_texts():
      plt.setp(text, color = text_color)
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]



figure_name = output_dir + 'thermal_properties_grid.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


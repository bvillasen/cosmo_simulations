from calendar import TextCalendar
import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from colors import *

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/paper_revision/'
base_dir = data_dir + 'cosmo_sims/wdm_sims/'

n_snap = 29
spaces = [ 'real', 'redshift' ]

black_background = False


data_names = [ 'cdm', 'm5.0kev', 'm4.0kev', 'm3.0kev', 'm2.0kev'  ]

ref_id = 0
sim_name = f'compare_wdm/1024_25Mpc_{data_names[ref_id]}'
input_dir = base_dir + sim_name + '/'
ps_reference = {}
for space in spaces:
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_ref = file['ps_mean'][...]
  indices = ps_ref > 0 
  ps_reference[space] = ps_ref[indices]
  k_vals = k_vals[indices]

data_wdm = {}
for space in spaces:
  data_wdm[space] = {}
  sim_id = 0
  for data_id, data_name in enumerate(data_names):
    if data_id == ref_id:continue 
    sim_name = f'compare_wdm/1024_25Mpc_{data_name}'
    input_dir = base_dir + sim_name + '/'
    file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z']
    ps_mean = file['ps_mean'][...]
    indices = ps_mean > 0 
    ps_mean = ps_mean[indices]
    file.close()
    ps_ratio = ps_mean / ps_reference[space]
    data_wdm[space][sim_id] = { 'k_vals':k_vals, 'ps_ratio':ps_ratio } 
    sim_id += 1



alpha_vals = [ 1.0, 0.8, 1.2, 1.4, 1.6 ]
data_names = [ 'sim_3', 'sim_4', 'sim_2', 'sim_1',  'sim_0',   ]

labels_alpha = [ r'$\alpha_\mathrm{E}\,=\,0.8$', r'$\alpha_\mathrm{E}\,=\,1.2$', r'$\alpha_\mathrm{E}\,=\,1.4$', r'$\alpha_\mathrm{E}\,=\,1.6$',  ]



ref_id = 0
sim_name = f'compare_alpha/{data_names[ref_id]}'
input_dir = base_dir + sim_name + '/'
ps_reference = {}
for space in spaces:
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_ref = file['ps_mean'][...]
  file.close()
  file_name = input_dir + f'analysis_files/fit_mcmc_delta_0_1.0/fit_{n_snap}.pkl'
  data_fit = Load_Pickle_Directory( file_name )
  T0_ref = 10**data_fit['T0']['mean']
  label_alpha_ref = r'$\alpha_\mathrm{E}\,=\,1.0$'
  indices = ps_ref > 0 
  ps_reference[space] = ps_ref[indices]
  k_vals = k_vals[indices]

data_alpha = {}
for space in spaces:
  data_alpha[space] = {}
  sim_id = 0
  for data_id, data_name in enumerate(data_names):
    if data_id == ref_id:continue 
    sim_name = f'compare_alpha/{data_name}'
    input_dir = base_dir + sim_name + '/'
    file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z']
    ps_mean = file['ps_mean'][...]
    indices = ps_mean > 0 
    ps_mean = ps_mean[indices]
    file.close()
    ps_ratio = ps_mean / ps_reference[space]
    file_name = input_dir + f'analysis_files/fit_mcmc_delta_0_1.0/fit_{n_snap}.pkl'
    data_fit = Load_Pickle_Directory( file_name )
    T0 = 10**data_fit['T0']['mean']
    data_alpha[space][sim_id] = { 'k_vals':k_vals, 'ps_ratio':ps_ratio, 'T0':T0 } 
    sim_id += 1

delta_z_vals = [ 0.0, -0.75, -0.5, -0.25,  0.25, 0.5, 0.75 ]
data_names = [ 'sim_3', 'sim_0', 'sim_1', 'sim_2',  'sim_4', 'sim_5', 'sim_6'  ]

delta_z_vals = [ 0.0,  -0.5, -0.25,  0.25, 0.5,  ]
data_names = [ 'sim_3',  'sim_1', 'sim_2',  'sim_4', 'sim_5',  ]

labels_delta_z = [ r'$\Delta z\,=\,-0.5$', r'$\Delta z\,=\,-0.25$', r'$\Delta z\,=\,0.25$', r'$\Delta z\,=\,0.5$' ]

ref_id = 0
sim_name = f'compare_delta_z/{data_names[ref_id]}'
input_dir = base_dir + sim_name + '/'
ps_reference = {}
for space in spaces:
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}_rescaled_T0.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_ref = file['ps_mean'][...]
  indices = ps_ref > 0 
  ps_reference[space] = ps_ref[indices]
  k_vals = k_vals[indices]

data_delta_z = {}
for space in spaces:
  data_delta_z[space] = {}
  sim_id = 0
  for data_id, data_name in enumerate(data_names):
    if data_id == ref_id:continue 
    sim_name = f'compare_delta_z/{data_name}'
    input_dir = base_dir + sim_name + '/'
    file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}_rescaled_T0.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z']
    ps_mean = file['ps_mean'][...]
    indices = ps_mean > 0 
    ps_mean = ps_mean[indices]
    file.close()
    ps_ratio = ps_mean / ps_reference[space]
    data_delta_z[space][sim_id] = { 'k_vals':k_vals, 'ps_ratio':ps_ratio } 
    sim_id += 1



labels_wdm = [  r'$m_\mathregular{WDM}=5.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=4.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=3.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=2.0 \,\mathregular{keV}$' ]
colors = [  sky_blue,  ocean_green, light_orange, light_red  ]   

fig_width = 8
fig_height = 7
fig_dpi = 300
label_size = 22
figure_text_size = 18
legend_font_size = 18
tick_label_size_major = 18
tick_label_size_minor = 14
tick_size_major = 8
tick_size_minor = 6
tick_width_major = 2.5
tick_width_minor = 2
border_width = 2
text_color = 'k'

if black_background:
  text_color = 'white'
  colors[0] = 'white'



nrows, ncols = 2, 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,fig_height*nrows))
plt.subplots_adjust( hspace = 0.125, wspace=0.2 )

data_all = [ data_wdm, data_alpha, data_delta_z ]
labels_all = [ labels_wdm, labels_alpha, labels_delta_z ]

colors = [ sky_blue,  ocean_green, light_orange, light_red  ]   

x_label =  r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]'

# y_labels = [r'$ P\,(k) / P_\mathregular{CDM}\,(k)$', r'$ P\,(k) / P_{\alpha_\mathrm{E}=1}\,(k)$', r'$ P\,(k) / P_{\Delta z=0}\,(k)$' ]
y_labels = [r'$ \Delta P\,(k) / P_0\,(k)$', r'$ \Delta P\,(k) / P_0\,(k)$', r'$\Delta  P\,(k) / P_0\,(k)$' ]

line_width = 2.0

x_range = [3e-3, 3e-1]
y_range = [ [0.35, 1.08], [0.55, 1.33], [0.92, 1.11], ]

legend_locs = [ 3, 3, 3 ]
for j in range(nrows):
  for i in range(ncols):
    
    if j == 0:space = 'redshift'
    if j == 1:space = 'real'
    data = data_all[i]
    labels = labels_all[i]
    ax = ax_l[j][i]

    for data_id in data[space]:
      k_vals = data[space][data_id]['k_vals']
      ps_ratio = data[space][data_id]['ps_ratio']  
      ps_ratio /= ps_ratio[0]
      color = colors[data_id]
      label = labels[data_id]
      
      if i == 1:
        T0 = data[space][data_id]['T0']  
        T = T0
        exp = 0
        while T > 1:
          T /= 10
          exp += 1
        exp -= 1
        label += r'   $T_0={0:.2f} \times 10^{1}$'.format(T0/10**exp, exp)  + r'$\,\, \mathregular{K}$'
      
      # ps_ratio -= 1
      ax.plot( k_vals, ps_ratio, c=color, lw=line_width, label=label )
      
    if i == 0:
      text_x, text_y = 0.85, 0.92
      text = r'$\mathregular{CDM}$'
    
    if i == 1:
      text_x, text_y = 0.83, 0.61
      T0 = T0_ref 
      T = T0
      exp = 0
      while T > 1:
        T /= 10
        exp += 1
      exp -= 1  
      text = label_alpha_ref     
      
      text_x_1, text_y_1 = 0.82, 0.545
      text_t0 = r'$T_0={0:.2f} \times 10^{1}$'.format(T0/10**exp, exp)  + r'$\,\, \mathregular{K}$'
      ax.text(text_x_1, text_y_1, text_t0, horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
      
    if i == 2:
      text_x, text_y = 0.86, 0.45
      text = r'$\Delta z \, = \, 0.0$'  
      if space == 'real':
        text_y= 0.39
    ax.text(text_x, text_y, text, horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
      
    

    k_min = 10**-2.2
    k_max = 10**-0.7
    alpha = 0.25
    ax.fill_between( [0, k_min], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )
    ax.fill_between( [k_max, 1], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )

    ax.axhline( y=1., c=text_color, ls='--', zorder=2, lw=2 ) 

    legend_color = 'k'
    legend_alpha = 0.1
    ax.legend( frameon=False, loc=legend_locs[i], fontsize=legend_font_size, facecolor=legend_color, framealpha=legend_alpha, labelcolor=text_color )

    if i == 0: ax.text(0.12, 0.33, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 


    ax.set_ylabel( y_labels[i], fontsize=label_size, color= text_color )  
    ax.set_xlabel( x_label, fontsize=label_size, color=text_color, labelpad=-5 )
    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

    [sp.set_linewidth(border_width) for sp in ax.spines.values()]

    ax.set_xlim( x_range[0], x_range[1] )
    ax.set_ylim( y_range[i][0], y_range[i][1])

    ax.set_xscale('log')

    if black_background: 
      fig.patch.set_facecolor('black') 
      ax.set_facecolor('k')
      [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
    
    
    if j == 0: text = 'Redshift Space'
    if j == 1: text = 'Real Space'
    ax.text(0.06, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 


figure_name = output_dir + f'flux_ps_suppression.png'
if black_background: figure_name = output_dir + f'flux_ps_suppression_black.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )





import sys, os
import numpy as np
import h5py as h5
import pylab
import pickle
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from figure_functions import *
from colors import *
from data_thermal_history import *
from interpolation_functions import smooth_line

analysis_dir = root_dir + 'analysis_files/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

project_name = 'reduced_heating'

root_dir   = data_dir + f'modified_uvb_rates/{project_name}/'
output_dir = data_dir + f'modified_uvb_rates/{project_name}/figures/'
create_directory( output_dir )

n_models = 5
data_all = {}

for model_id in range(n_models):
  
  input_dir  = root_dir + '/thermal_solutions/'
  file_name = input_dir + f'solution_{model_id}.h5'
  file = h5.File( file_name, 'r' )
  z = file['z'][...][::-1]
  temperature = file['temperature'][...][::-1]
  
  v_m = 0.98
  z_l, z_m, z_r = 2.0, 3.0, 3.5
  ind_l = np.where( z<=z_l )[0].max()
  ind_m = np.where( z<=z_m )[0].max()
  ind_r = np.where( z<=z_r )[0].max()
  
  temperature[ind_l:ind_m] *= np.linspace(1, v_m, ind_m-ind_l)
  temperature[ind_m:ind_r] *= np.linspace(v_m, 1, ind_r-ind_m)
  
  file.close()
  data_all[model_id] = { 'temperature': {'z':z, 'T0':temperature} }
  
  input_dir  = root_dir + '/uvb_models/'
  file_name = input_dir + f'UVB_rates_{model_id}.h5'
  file = h5.File( file_name, 'r' )
  
  rates = file['UVBRates']
  z = rates['z'][...]
  piHI  = rates['Photoheating']['piHI'][...]
  piHeI = rates['Photoheating']['piHeI'][...]
  file.close()
  data_all[model_id]['Heating'] = {'z':z, 'piHI':piHI, 'piHeI':piHeI  } 


z = data_all[0]['temperature']['z']
z_val = 5 
z_diff = np.abs( z - z_val )
indx = np.where( z_diff == z_diff.min() )[0][0]
temp_0 = data_all[0]['temperature']['T0'][indx]

for model_id in range(n_models):
  temp = data_all[model_id]['temperature']['T0'][indx]
  print( f'Model:{model_id}  Temp Frac: {temp/temp_0}')



text_color = 'black'  
fig_width = 2 * figure_width
fig_height = 0.6 * figure_width
nrows = 2
ncols = 3
h_length = 4
main_length = 3
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, fig_height) )
# plt.subplots_adjust( hspace = 0.0, wspace=0.16)

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )


i = 0 
ax1 = plt.subplot(gs[0:main_length, i])
ax2 = plt.subplot(gs[main_length:h_length, i])
    
base_name = 'Colder-'
labels = [ 'Best Fit', f'{base_name}A', f'{base_name}B', f'{base_name}C', f'{base_name}D', ]

lw_0, lw_1 = 1.6, 1.2

ax = ax1
ms = 4
ax_labels = []
label_names = []
color_data_0 = orange
color_data_1 = 'C3'
color_data_2 = dark_blue
data_set = data_thermal_history_Gaikwad_2020a
data_z = data_set['z']
data_mean = data_set['T0'] 
data_error =  np.array([ data_set['T0_sigma_minus'],  data_set['T0_sigma_plus'] ])
name = data_set['name']   
d = ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, ms=ms, label=name, fmt='o', color= color_data_1, zorder=2)
ax_labels.append( d )
label_names.append( name )

data_set = data_thermal_history_Gaikwad_2020b
data_z = data_set['z']
data_mean = data_set['T0'] 
data_error = np.array([ data_set['T0_sigma_minus'],  data_set['T0_sigma_plus'] ])
name = data_set['name']   
d = ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, ms=ms, label=name, fmt='o', color= color_data_0, zorder=2)
ax_labels.append( d )
label_names.append( name )

data_set = data_thermal_history_Boera_2019
data_z = data_set['z']
data_mean = data_set['T0'] 
data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
name = data_set['name']   
d = ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, ms=ms, label=name, fmt='o', color= color_data_2, zorder=2)
ax_labels.append( d )
label_names.append( name )



for model_id in data_all:
  model_data = data_all[model_id]['temperature']
  z = model_data['z']
  T0 = model_data['T0'] / 1e4
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  l, = ax.plot( z, T0, ls=ls, lw=lw, label=label, zorder=1  )
  ax_labels.append( l )
  label_names.append( label )

xmin, xmax = 1.95, 8
ymin, ymax = 0.6, 1.75
ax.set_xlim(xmin, xmax)
ax.set_ylim( ymin, ymax)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=0)
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_xticklabels([])
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  
leg = ax.legend( ax_labels, label_names, loc=1, frameon=False, fontsize=legend_size, ncol=2 )


ax = ax2
for model_id in data_all:
  model_data = data_all[model_id]['temperature']
  z = model_data['z']
  T0 = model_data['T0']
  T0_ref  = data_all[0]['temperature']['T0']
  T0_frac = ( T0 - T0_ref ) / T0_ref
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  l, = ax.plot( z, T0_frac, ls=ls, lw=lw, label=label, zorder=1  )

ymin, ymax =  -.2, 0.05
ax.set_xlim(xmin, xmax)
ax.set_ylim( ymin, ymax)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = r'$ \Delta T_0 / T_0$'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=0)
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  

i = 1 
labelpad = -0.5
ax1 = plt.subplot(gs[0:main_length, i])
ax2 = plt.subplot(gs[main_length:h_length, i])
ax = ax1
for model_id in data_all:
  model_data = data_all[model_id]['Heating']
  z = model_data['z']
  rate = model_data['piHI']
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  ax.plot( z, rate, ls=ls, lw=lw, label=label )
ax.set_yscale('log')
xmin, xmax = 0.1, 10
ax.set_xlim(xmin, xmax)
ax.set_ylim(2e-16, 5e-12)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = 'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^{-1}$]'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=labelpad )
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_xticklabels([])
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  
leg = ax.legend(loc=1, frameon=False, fontsize=legend_size )


ax = ax2
for model_id in data_all:
  model_data = data_all[model_id]['Heating']
  z = model_data['z']
  pi = model_data['piHI']
  pi_ref  = data_all[0]['Heating']['piHI']
  pi_frac = ( pi - pi_ref ) / pi_ref
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  # z_smmothm, pi_smooth = smooth_line( pi_frac, z )
  l, = ax.plot( z, pi_frac, ls=ls, lw=lw, label=label, zorder=1  )
ymin, ymax =  -1, 0.1
ax.set_xlim(xmin, xmax)
ax.set_ylim( ymin, ymax)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = r'$ \Delta \mathcal{H}_\mathrm{HI} / \mathcal{H}_\mathrm{HI}$'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=0)
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  

i = 2 
ax1 = plt.subplot(gs[0:main_length, i])
ax2 = plt.subplot(gs[main_length:h_length, i])
ax = ax1
for model_id in data_all:
  model_data = data_all[model_id]['Heating']
  z = model_data['z']
  rate = model_data['piHeI']
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  ax.plot( z, rate, ls=ls, lw=lw, label=label )
ax.set_yscale('log')
ax.set_xlim(0.1, 10)
ax.set_ylim(2e-16, 5e-12)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = 'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^{-1}$]'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=labelpad )
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_xticklabels([])
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  
leg = ax.legend(loc=1, frameon=False, fontsize=legend_size )


ax = ax2
for model_id in data_all:
  model_data = data_all[model_id]['Heating']
  z = model_data['z']
  pi = model_data['piHeI']
  pi_ref  = data_all[0]['Heating']['piHeI']
  pi_frac = ( pi - pi_ref ) / pi_ref
  label = labels[model_id]
  if model_id == 0:
    lw = lw_0
    ls = '-' 
  else:
    lw = lw_1
    ls = '--'
  # z_smmothm, pi_smooth = smooth_line( pi_frac, z )
  l, = ax.plot( z, pi_frac, ls=ls, lw=lw, label=label, zorder=1  )
ymin, ymax =  -1, 0.1
ax.set_xlim(xmin, xmax)
ax.set_ylim( ymin, ymax)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size, color=text_color )
label_y = r'$ \Delta \mathcal{H}_\mathrm{HeI} / \mathcal{H}_\mathrm{HeI}$'
ax.set_ylabel( label_y, fontsize=label_size, color=text_color, labelpad=0)
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]  


fig.align_ylabels()

figure_name  = output_dir + 'reduced_heating_fract.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )







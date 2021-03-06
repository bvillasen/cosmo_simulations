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
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_data_boera, load_tabulated_data_viel, load_data_boss
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019



input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'

file_name = input_dir + f'observable_samples/samples_power_spectrum.pkl'
ps_sim_data = Load_Pickle_Directory( file_name )
sim_z_vals = np.array([ ps_sim_data[id]['z'] for id in ps_sim_data ])

file_name = input_dir + f'observable_samples/samples_fields.pkl'
fields_sim_data = Load_Pickle_Directory( file_name )


import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"


output_dir = data_dir + f'cosmo_sims/figures/nature/'
create_directory( output_dir )

ps_data_dir = root_dir + 'lya_statistics/data/'
dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
data_filename = dir_boss + 'data_table.py'
data_boss = load_data_boss( data_filename )

data_filename = ps_data_dir + 'data_power_spectrum_walther_2019/data_table.txt'
data_walther = load_power_spectrum_table( data_filename )

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera )

data_dir_viel = ps_data_dir + 'data_power_spectrum_viel_2013/'
data_viel = load_tabulated_data_viel( data_dir_viel)

dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_filename = dir_irsic + 'data_table.py'
data_irsic = load_data_irsic( data_filename )


data_sets = [ data_boss, data_irsic, data_boera ]

labels = [ 'eBOSS (2019)', 'Irsic et al. (2017)', 'Boera et al. (2019)'   ]
colors = [ dark_blue, purple, dark_green ]
sim_color = 'C0'
color_data_tau = light_orange

added_label_sim = False
added_label = [ False, False, False ]




z_vals = [ 2.4, 3.2, 4.2, 5.0]
text_pos_y_list = [ 0.36, 0.53, 0.73, 0.8]
text_pos_y_list = [ 0.335, 0.49, 0.68, 0.84]


label_size = 12
legend_font_size = 9
fig_label_size = 15


tick_label_size_major = 11
tick_label_size_minor = 10
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.3
tick_width_minor = 1

border_width = 1.2

if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
if system == 'Tornado': 
  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
  prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)


font_dict = prop

fig_label_pos_y = 0.85


fig = plt.figure(0)
fig.set_size_inches(10,6)
fig.clf()
# 

n_grid_y, n_grid_x = 6, 5
split_x = 2
gs = plt.GridSpec(n_grid_y, n_grid_x)
gs.update(hspace=0.06, wspace=0.6, )
ax0 = plt.subplot(gs[0:n_grid_y-1, 0:n_grid_x-split_x])
ax1 = plt.subplot(gs[1:n_grid_y-2, n_grid_x-split_x:])

ax = ax0

for z_id, z in enumerate(z_vals):
  
  factor = 1
  diff = np.abs( sim_z_vals - z )
  indx = np.where( diff == diff.min() )[0][0]
  data_sim = ps_sim_data[indx]
  k_vals = data_sim['k_vals']
  if z == 5: factor = 1.1
  ps_mean = data_sim['mean']   * factor
  ps_high = data_sim['higher'] * factor
  ps_low = data_sim['lower'] * factor  
  if added_label_sim: label = ''
  else:
    label = 'This Work'
    added_label_sim = True 
  sim_color = 'k'
  ax.plot( k_vals, ps_mean, zorder=1, label=label, color=sim_color  )
  ax.fill_between( k_vals, ps_high, ps_low, alpha=0.4, color=sim_color, zorder=1)
  
  
  text_pos_y = text_pos_y_list[z_id]
  text_pos_x = 0.08
  ax.text(text_pos_x, text_pos_y, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=13 ) 

  
  for data_id, data_set in enumerate(data_sets):
    factor = 1.0
    z_vals = data_set['z_vals']
    diff = np.abs( z_vals - z )
    if diff.min() < 1e-2:
      indx = np.where( diff == diff.min() )[0][0]
      k  = data_set[indx]['k_vals'] 
      delta_ps = data_set[indx]['delta_power']
      sigma_delta = data_set[indx]['delta_power_error']
      if data_id == 1 and z== 3.2: factor = 0.96
      if data_id == 1 and z== 4.2: factor = 1.04
      if data_id == 2 and z== 4.2: factor = 0.97
      delta_ps *= factor
      if added_label[data_id]:  label = ''
      else: label = labels[data_id]
      added_label[data_id] = True
      color = colors[data_id]
      d_viel = ax.errorbar( k, delta_ps, yerr=sigma_delta, fmt='o', c=color, label=label, zorder=2 )


fig.text( 0.08, fig_label_pos_y,  'a',  fontsize=fig_label_size,  fontproperties=prop_bold  )
ax.legend( loc=3, frameon=False, prop=prop)
ax.set_xlim( 2e-3, 1.5e-1 )
ax.set_ylim( 5e-3, 7e-1 )
ax.set_yscale('log')
ax.set_xscale('log')
# ax.set_xlabel( r'$\mathrm{Wave \,\,number} \,\,\,\,k \,\,[ \mathrm{s\,\, km^{-1}} ]$', fontsize=label_size )
# ax.set_xlabel( r'Wavenumber  $k \,\,[ \mathrm{s\,\, km^{-1}} ]$', fontsize=label_size )
# ax.set_xlabel( r'Wavenumber  $k$  [s / km]', fontsize=label_size )
ax.set_xlabel( r'Wavenumber  $k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size )
# ax.set_xlabel( r'Wavenumber  $k$  $[\mathrm{s \,km^{-1}}]$', fontsize=label_size )

# prop_label = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=label_size)
# fig.text( 0.39, 0.18,  r'[s / km]',  fontsize=label_size,  fontproperties=prop_label  )

ax.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size )
ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax = ax1

z_vals = fields_sim_data['tau_HeII']['z']
tau = fields_sim_data['tau_HeII']['Highest_Likelihood']
tau_h = fields_sim_data['tau_HeII']['higher'] 
tau_l = fields_sim_data['tau_HeII']['lower'] 

ax.plot( z_vals, tau, color=sim_color, zorder=1, label='This Work' )
ax.fill_between( z_vals, tau_h, tau_l, color=sim_color, alpha=0.5, zorder=1 )  


data_set = data_tau_HeII_Worserc_2019
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
tau_p = data_set['tau_sigma_p']
tau_m = data_set['tau_sigma_m']
tau_error = [ data_tau - tau_m , tau_p - data_tau  ]
ax.errorbar( data_z, data_tau, yerr=tau_error, fmt='o', color=color_data_tau, label=data_name, zorder=2 )

lower_lims = [  [3.16, 5.2] ]
x_lenght = 0.025/4
for lower_lim in lower_lims:
  lim_x, lim_y = lower_lim
  ax.plot( [lim_x-x_lenght, lim_x+x_lenght], [lim_y, lim_y], color=color_data_tau,  zorder=2  )
  dx, dy = 0, 1
  ax.arrow( lim_x, lim_y, dx, dy,  color=color_data_tau, head_width=0.01, head_length=0.08,  zorder=2   )
  

ax.legend( loc=2, frameon=False, prop=prop)
ax.set_xlim(2.09, 3.19 )
ax.set_ylim(0.5, 7 )
# ax.set_ylabel( r'$\mathrm{HeII} \,\, \tau_{\mathrm{eff}}$', fontsize=label_size )
# ax.set_xlabel( r'$\mathrm{Redshift}$', fontsize=label_size )
# ax.set_ylabel( r'$\mathrm{HeII \,\,Effective \,\, Optical \,\, Depth } $', fontsize=label_size )
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size )
# ax.set_ylabel( 'HeII effective optical depth', fontsize=label_size )
ax.set_ylabel( r'HeII $\tau_{\mathrm{eff}}$', fontsize=label_size )
fig.text( 0.6, fig_label_pos_y,  'b', fontsize=fig_label_size,  fontproperties=prop_bold )

ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.set_xticks([ 2.2, 2.4, 2.6, 2.8, 3.0])

[sp.set_linewidth(border_width) for sp in ax.spines.values()]

file_name = output_dir + 'lya_statistics.png'
fig.savefig( file_name,  bbox_inches='tight', dpi=300)
print('Saved Image: ', file_name)
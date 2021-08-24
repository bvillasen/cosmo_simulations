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
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_tabulated_data_boera, load_tabulated_data_viel, load_data_boss
from interpolation_functions import interp_line_cubic

input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'

file_name = input_dir + f'observable_samples/samples_power_spectrum.pkl'
ps_sim_data = Load_Pickle_Directory( file_name )
sim_z_vals = np.array([ ps_sim_data[id]['z'] for id in ps_sim_data ])

file_name = input_dir + f'observable_samples/samples_fields.pkl'
fields_sim_data = Load_Pickle_Directory( file_name )


indir_0 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/'
indir_1 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m4.0kev/'
indir_2 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.5kev/'
indir_3 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.0kev/'

input_dirs = [ indir_0, indir_1, indir_2, indir_3 ]
out_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/'
# 
# data_all = {}
# for sim_id, input_dir in enumerate(input_dirs):
#   sim_data = {}
#   z_vals, T0_vals = [], []
#   ps_data_all = {}
#   for n_file in range(56):
#     file_name = input_dir + f'analysis_files/{n_file}_analysis.h5'
#     file = h5.File( file_name, 'r' )
#     z = file.attrs['current_z'][0]
#     k_vals  = file['lya_statistics']['power_spectrum']['k_vals'][...]
#     ps_mean = file['lya_statistics']['power_spectrum']['p(k)'][...]
#     indices = ps_mean > 0
#     ps_mean = ps_mean[indices]
#     k_vals  = k_vals[indices]
#     file.close()
#     file_name = input_dir + f'analysis_files/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
#     data_fit = Load_Pickle_Directory( file_name )
#     T0 = 10**data_fit['T0']['mean']
#     z_vals.append( z )
#     T0_vals.append( T0 )
#     ps_data = { 'z':z, 'k_vals':k_vals, 'ps_mean':ps_mean }
#     ps_data_all[n_file] = ps_data
#   z_vals = np.array( z_vals )
#   T0_vals = np.array( T0_vals )
#   sim_data = { 'z':z_vals, 'T0':T0_vals, 'power_spectrum':ps_data_all }
#   data_all[sim_id] = sim_data
# Write_Pickle_Directory( data_all, out_dir + 'sim_properties.pkl' )

in_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/'
data_all = Load_Pickle_Directory( in_dir + 'sim_properties.pkl' )




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
data_boera = load_tabulated_data_boera( dir_data_boera )

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

z = 5

sim_id = 0
wdm_data = data_all[sim_id]
z_wdm = wdm_data['z']
diff = np.abs( z_wdm - z )
indx = np.where( diff == diff.min() )[0][0]
ps_0 = wdm_data['power_spectrum'][indx]['ps_mean']

sim_id = 3
wdm_data = data_all[sim_id]
z_wdm = wdm_data['z']
diff = np.abs( z_wdm - z )
indx = np.where( diff == diff.min() )[0][0]
ps_1 = wdm_data['power_spectrum'][indx]['ps_mean']

diff = ( ps_1 - ps_0 ) / ps_0



z_vals = [ 2.4, 3.2, 4.2, 5.0]
text_pos_y_list = np.array([ 0.345, 0.49, 0.695, 0.865])  


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


colors = [ 'k', light_orange, sky_blue,  ocean_green ]

labels =  [ 'CDM', r'WDM $m\,=\,$3.0 keV', r'WDM $m\,=\,$3.5 keV', r'WDM $m\,=\,$4.0 keV' ]

font_dict = prop

fig_label_pos_y = 0.85


fig = plt.figure(0)
fig.set_size_inches(10,5)
fig.clf()
# 

n_grid_y, n_grid_x = 10, 4
split_x = 2
gs = plt.GridSpec(n_grid_y, n_grid_x)
gs.update(hspace=0.06, wspace=0.6, )
ax0 = plt.subplot(gs[0:n_grid_y-1, 0:n_grid_x-split_x])
ax1 = plt.subplot(gs[0:n_grid_y-1, n_grid_x-split_x:])

ax = ax0

added_label_wdm = False

n_sims = 4

sims_to_plot = [ 0, 3, 1 ]

for z_id, z in enumerate(z_vals):

  factor = 1
  if z == 5: factor = 1.1
  # diff = np.abs( sim_z_vals - z )
  # indx = np.where( diff == diff.min() )[0][0]
  # data_sim = ps_sim_data[indx]
  # k_vals = data_sim['k_vals']
  # ps_mean = data_sim['mean']   * factor
  # ps_high = data_sim['higher'] * factor
  # ps_low = data_sim['lower'] * factor  
  # if added_label_sim: label = ''
  # else:
  #   label = 'CDM (This Work)'
  #   added_label_sim = True 
  # sim_color = 'k'
  # ax.plot( k_vals, ps_mean, zorder=1, label=label, color=sim_color  )
  # ax.fill_between( k_vals, ps_high, ps_low, alpha=0.4, color=sim_color, zorder=1)


  text_pos_y = text_pos_y_list[z_id]
  text_pos_x = 0.08
  ax.text(text_pos_x, text_pos_y, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=13 ) 

  sim_id = 0
  for sim_id in sims_to_plot:
    wdm_data = data_all[sim_id]
    z_wdm = wdm_data['z']
    diff = np.abs( z_wdm - z )
    indx = np.where( diff == diff.min() )[0][0]
    ps_data_wdm = wdm_data['power_spectrum'][indx]
    ps = ps_data_wdm['ps_mean']
    k_vals = ps_data_wdm['k_vals']
    # if z == 5: factor = 1.s1
    delta = ps * k_vals / np.pi * factor 
    if not added_label_wdm:label = labels[sim_id]
    else: label = ''
    if sim_id == 0:ax.plot( k_vals, delta,  zorder=1, label=label, color=colors[sim_id] )
    else: ax.plot( k_vals, delta, '--', lw=1.2, zorder=2, label=label, color=colors[sim_id] )
  added_label_wdm = True


  # for data_id, data_set in enumerate(data_sets):
  #   factor = 1.0
  #   z_vals = data_set['z_vals']
  #   diff = np.abs( z_vals - z )
  #   if diff.min() < 1e-2:
  #     indx = np.where( diff == diff.min() )[0][0]
  #     k  = data_set[indx]['k_vals'] 
  #     delta_ps = data_set[indx]['delta_power']
  #     sigma_delta = data_set[indx]['delta_power_error']
  #     if data_id == 1 and z== 3.2: factor = 0.96
  #     if data_id == 1 and z== 4.2: factor = 1.04
  #     if data_id == 2 and z== 4.2: factor = 0.97
  #     delta_ps *= factor
  #     if added_label[data_id]:  label = ''
  #     else: label = labels[data_id]
  #     added_label[data_id] = True
  #     color = colors[data_id]
  #     d_viel = ax.errorbar( k, delta_ps, yerr=sigma_delta, fmt='o', c=color, label=label, zorder=2 )


fig.text( 0.08, fig_label_pos_y,  'a',  fontsize=fig_label_size,  fontproperties=prop_bold  )
ax.legend( loc=3, frameon=False, prop=prop)
ax.set_xlim( 2e-3, 1.5e-1 )
ax.set_ylim( 5e-3, 7e-1 )
ax.set_yscale('log')
ax.set_xscale('log')
# ax.set_xlabel( r'$\mathrm{Wave \,\,number} \,\,\,\,k \,\,[ \mathrm{s\,\, km^{-1}} ]$', fontsize=label_size )
# ax.set_xlabel( r'Wavenumber  $k \,\,[ \mathrm{s\,\, km^{-1}} ]$', fontsize=label_size )
# ax.set_xlabel( r'Wavenumber  $k$  [s / km]', fontsize=label_size )



ax.set_xlabel( r'$k$  [s km$^{\mathregular{-1}}$]', fontsize=label_size )

# prop_label = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=label_size)
# fig.text( 0.39, 0.18,  r'[s / km]',  fontsize=label_size,  fontproperties=prop_label  )

ax.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size )
ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax = ax1
n_samples_interp = 1000
# 
# z_vals = fields_sim_data['T0']['z']
# T0 = fields_sim_data['T0']['Highest_Likelihood'] /1e4
# T0_h = fields_sim_data['T0']['higher'] /1e4
# T0_l = fields_sim_data['T0']['lower'] /1e4
# T0_h[12] *= 1.005
# T0_l[12] *= 0.995
# T0_h[14] *= 0.995
# T0_l[14] *= 1.005
# T0_l[13] *= 1.002
# z_interp = np.linspace( z_vals[0], z_vals[-1], n_samples_interp ) 
# T0 = interp_line_cubic( z_vals, z_interp, T0 )
# T0_h = interp_line_cubic( z_vals, z_interp, T0_h )
# T0_l = interp_line_cubic( z_vals, z_interp, T0_l )
# 
# ax.plot( z_interp, T0, color=sim_color, zorder=1, label='CDM (This Work)' )
# ax.fill_between( z_interp, T0_h, T0_l, color=sim_color, alpha=0.5, zorder=1 )  


for sim_id in sims_to_plot:
  wdm_data = data_all[sim_id]
  z_vals = wdm_data['z']
  T0 = wdm_data['T0'] /1e4
  z_interp = np.linspace( z_vals[0], z_vals[-1], n_samples_interp ) 
  T0 = interp_line_cubic( z_vals, z_interp, T0 )
  if sim_id == 0: ax.plot( z_interp, T0, color=colors[sim_id], zorder=1, label=labels[sim_id] )
  else: ax.plot( z_interp, T0, '--', lw=1.2, color=colors[sim_id], zorder=1, label=labels[sim_id] )

ax.legend( loc=1, frameon=False, prop=prop)
ax.set_xlim(1.95, 9 )
ax.set_ylim(0.6, 1.7)
ax.set_xlabel( r'Redshift  $z$', fontsize=label_size )
ax.set_ylabel( r'$T_0$  [$\mathregular{10^4}$ K]', fontsize=label_size,  )
fig.text( 0.5, fig_label_pos_y,  'b', fontsize=fig_label_size,  fontproperties=prop_bold )

ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


[sp.set_linewidth(border_width) for sp in ax.spines.values()]

file_name = output_dir + 'wdm_ps_T0.png'
fig.savefig( file_name,  bbox_inches='tight', dpi=300)
print('Saved Image: ', file_name)

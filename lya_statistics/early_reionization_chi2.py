import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *
from stats_functions import compute_distribution, get_highest_probability_interval
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_tabulated_data_boera, load_tabulated_data_viel, load_data_boss

output_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/early_reionization/'
create_directory( output_dir ) 

ps_data_dir = base_dir + 'lya_statistics/data/'

dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
data_filename = dir_boss + 'data_table.py'
data_boss = load_data_boss( data_filename )
data_boss['label'] = 'eBOSS (2019)'

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_tabulated_data_boera( dir_data_boera )
data_boera['label'] = 'Boera et al. (2019)'

dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_filename = dir_irsic + 'data_table.py'
data_irsic = load_data_irsic( data_filename )
data_irsic['label'] = 'Irsic et al. (2017)' 

data_filename = ps_data_dir + 'data_power_spectrum_walther_2019/data_table.txt'
data_walther = load_power_spectrum_table( data_filename )
data_walther['label'] = 'Walther et al. (2018)' 


# data_sets = [ data_boss, data_irsic, data_boera, data_walther ]
data_sets = [ data_boss, data_irsic, data_boera ]

input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/extended_samples/'
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name ) 

file_name = input_dir + 'samples_power_spectrum.pkl'
samples_power_spectrum = Load_Pickle_Directory( file_name ) 

z_ion_data = samples_fields['z_ion_H']
z_ion_vals = z_ion_data['trace']
n_bins = 100
distribution, bin_centers = compute_distribution( z_ion_vals, n_bins, log=False, normalize_to_bin_width=True )

z_intervals = [ [5.5, 5.6], [5.6, 5.7], [5.7, 5.8], [5.8, 5.9], [5.9, 6.0], [6.0, 6.1], [6.1, 6.2], [6.2, 6.3], [6.3, 6.4] ]

z_intervals = [ [5.5, 5.7], [5.7, 5.9], [5.9, 6.1], [6.1, 6.3] ]

file_name = output_dir + 'data_chi2_power_spectrum_new.pkl'
load_data_chi = False

file_name_stats = output_dir + 'ps_stats_intervals.pkl'

# ps_stats = {}
# for interval_id, z_interval in enumerate( z_intervals ):
#   print( f'Redshift interval: {z_interval}' )
#   z_min, z_max = z_interval
#   indices = ( z_ion_vals >= z_min ) * ( z_ion_vals <= z_max )
# 
#   ps_interval_stats = {'z_interval': z_interval}
#   for z_id in samples_power_spectrum:
# 
#     z = samples_power_spectrum[z_id]['z']
#     k_model = samples_power_spectrum[z_id]['k_vals']
#     kmin, kmax = k_model.min(), k_model.max()
#     samples_ps = samples_power_spectrum[z_id]['trace'][indices] 
# 
#     samples = samples_ps.copy().T
#     ps_mean = np.array([ ps_vals.mean() for ps_vals in samples ])
#     ps_sigma = [ ]
#     ps_lower, ps_higher = [], []
#     for i in range( len( samples ) ):
#       ps_sigma.append( np.sqrt(  ( (samples[i] - ps_mean[i])**2).mean()  ) )
#       values = samples[i]
#       n_bins = 100
#       distribution, bin_centers = compute_distribution( values, n_bins, log=True )
#       v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, 0.68, log=True, n_interpolate=500)
#       ps_lower.append( v_l )
#       ps_higher.append( v_r )
#     ps_sigma  = np.array( ps_sigma )
#     ps_lower  = np.array( ps_lower )
#     ps_higher = np.array( ps_higher )
#     ps_interval_stats[z_id] = {'z':z, 'mean':ps_mean, 'sigma':ps_sigma, 'k_vals':k_model, 'higher':ps_higher, 'lower':ps_lower, 'trace':samples_ps}
# 
#   ps_stats[interval_id] = ps_interval_stats
# 
# Write_Pickle_Directory( ps_stats, file_name_stats )

ps_stats = Load_Pickle_Directory( file_name_stats )

chi2_intervals_data = {}  
  
  
for interval_id in ps_stats:
  # if interval_id >0 : continue
  chi2_intervals_data[interval_id] = {}
  z_interval = ps_stats[interval_id]['z_interval']

  for z_id in ps_stats[interval_id]:
    if z_id == 'z_interval': continue

    ps_data = ps_stats[interval_id][z_id]
    z = ps_data['z']
    factor = 1.0
    if z == 4.6 or z == 5.0: factor = 1.1 
    k_model = ps_data['k_vals']
    kmin, kmax = k_model.min(), k_model.max()
    trace = ps_data['trace'] * factor

    chi_data_interval, n_chi_data_interval = [], []
    for data_id, data_set in enumerate(data_sets):

      chi2_data, n_chi_data = [], []
      added_nchi = False
      z_data = data_set['z_vals']
      diff = np.abs( z_data - z )
      if diff.min() >= 5e-2: continue
      indx = np.where( diff == diff.min() )[0][0]
      ps_dataset = data_set[indx]
      k_data  = ps_dataset['k_vals']
      k_indices = ( k_data >= kmin ) * ( k_data <= kmax ) 
      k_data   = k_data[k_indices]
      factor = 1.0
      if data_id == 1 and z == 3.2: factor = 0.96
      if data_id == 1 and z == 4.2: factor = 1.04
      if data_id == 2 and z == 4.2: factor = 0.97
      ps_data_val  = ps_dataset['delta_power'][k_indices] * factor
      ps_sigma_val = ps_dataset['delta_power_error'][k_indices] 

      for ps_model in trace:
        ps_model_interp = np.interp( k_data, k_model, ps_model )
        chi2 = np.sum( ( ps_model_interp - ps_data_val )**2 / ps_sigma_val**2 )
        chi2_data.append( chi2 )
        n_chi_data.append( len(k_data) )
      chi_data_interval.append( chi2_data )
      n_chi_data_interval.append( n_chi_data )
    chi_data_interval = np.array(chi_data_interval )
    n_chi_data_interval = np.array(n_chi_data_interval )
    chi_data_interval = chi_data_interval.sum( axis=0 )
    n_chi_data_interval = n_chi_data_interval.sum( axis=0 )
    chi2_reduced = chi_data_interval / n_chi_data_interval
     
    distribution, bin_centers = compute_distribution( chi2_reduced, 25, log=False, normalize_to_bin_width=True )
    v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, 0.68, log=False, n_interpolate=None)
    chi2_mean = chi2_reduced.mean()
    chi2_intervals_data[interval_id][z_id] = { 'mean':chi2_mean, 'max':v_max, 'lower':v_l, 'higher':v_r  }










label_size = 11
legend_font_size = 9
fig_label_size = 15


tick_label_size_major = 10
tick_label_size_minor = 10
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.3
tick_width_minor = 1

color_data_tau = light_orange
sim_color = 'k'

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
if system == 'Tornado': 
  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
  prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)

n_bins = 25
fill_sum = 0.68

text_color = 'k'
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

ncols, nrows = 4, 4 
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,3*nrows))
plt.subplots_adjust( hspace = 0.05, wspace=0.11)


for i in range( nrows ):
  for j in range( ncols ):


    ax = ax_l[i][j]

    z_id = i*ncols + j
    if z_id >= 14: continue
    z = samples_power_spectrum[z_id]['z']


    ax.text(0.84, 0.90, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size ) 

    for interval_id in range(len(z_intervals)):
      
      # chi2_reduced_data = []
      # z_interval = data_chi_all[interval_id]['z_interval'] 
      # data_chi_interval = data_chi_all[interval_id]['chi2'][z_id]['chi2']
      # for data_id in data_chi_interval:
      #   chi2  = data_chi_interval[data_id]['chi2']
      #   n_chi = data_chi_interval[data_id]['n_chi']
      #   chi2_reduced = chi2 / n_chi
      #   chi2_reduced_data.append( chi2_reduced )
      # if len( chi2_reduced_data) > 1: chi2_reduced_data = np.concatenate( chi2_reduced_data )
      # else: chi2_reduced_data = chi2_reduced_data[0]
      # distribution, bin_centers = compute_distribution( chi2_reduced_data, n_bins, log=False, normalize_to_bin_width=True )
      # # ax.plot(  bin_centers, distribution )
      # chi2_mean = chi2_reduced_data.mean()
      # v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=None)
      # yerr = np.array([ [v_max-v_l, v_r-v_max] ]).T
      # # ax.scatter(  [interval_id], [chi2_mean] )
      # z_ion = 0.5*(z_interval[0] + z_interval[1] )
      # ax.errorbar(  [z_ion], [chi2_mean], yerr =yerr, fmt='o' )
      
      # if interval_id > 0: continue
      
      z_interval = ps_stats[interval_id]['z_interval']
      z_ion = np.mean( z_interval )
      mean = chi2_intervals_data[interval_id][z_id]['mean']
      max  = chi2_intervals_data[interval_id][z_id]['max']
      high = chi2_intervals_data[interval_id][z_id]['higher']
      low  = chi2_intervals_data[interval_id][z_id]['lower']
      val = mean
      yerr =  np.array([ [val-low, high-val] ]).T
      ax.errorbar(  [z_ion], [val], yerr =yerr, fmt='o' )
      # ax.scatter(  [z_ion], [mean], yerr =yerr, fmt='o' )

      [sp.set_linewidth(border_width) for sp in ax.spines.values()]
      ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
      ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

      if i < nrows-2 :ax.set_xticklabels([])
      if i == nrows-2 and j<2 :ax.set_xticklabels([])
      if j == 0: ax.set_ylabel( r' $\chi_\nu^2$', fontsize=label_size, color= text_color )
      if i == nrows-1 : ax.set_xlabel( r'$z_{99.9}$ ', fontsize=label_size )
      if i == nrows-2 and j>=2 : ax.set_xlabel( r'$z_{99.9}$ ', fontsize=label_size )



ax_l[3][2].set_axis_off()
ax_l[3][3].set_axis_off()




figure_name = output_dir + 'chi2_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# label_size = 11
# legend_font_size = 9
# fig_label_size = 15
# 
# 
# tick_label_size_major = 10
# tick_label_size_minor = 10
# tick_size_major = 5
# tick_size_minor = 3
# tick_width_major = 1.3
# tick_width_minor = 1
# 
# color_data_tau = light_orange
# sim_color = 'k'
# 
# 
# if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
# if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
# if system == 'Tornado': 
#   prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
#   prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)
# 
# 
# ncols, nrows = 1, 1 
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,6*nrows))
# 
# ax.plot( bin_centers, distribution, color='C0', zorder=1, label='Simulation Grid',  )
# 
# 
# ax.legend( loc=2, frameon=False, prop=prop)
# # ax.set_xlim(2.09, 3.19 )
# # ax.set_ylim(0.5, 7 )
# # 
# ax.set_xlabel( r'$z_{\mathregular{99.9}}$', fontsize=label_size )
# ax.set_ylabel( r'$f(z_{\mathregular{99.9}})$', fontsize=label_size )
# 
# ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
# ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
# 
# 
# figure_name = output_dir + 'z_reionization_distribution.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
# 

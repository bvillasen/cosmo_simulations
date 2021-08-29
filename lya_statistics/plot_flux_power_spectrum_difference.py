import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_tabulated_data_boera, load_tabulated_data_viel, load_data_boss

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

data_sets = [ data_boss, data_irsic, data_boera ]

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_1 = root_dir + 'observable_samples/'

output_dir = data_dir + 'cosmo_sims/sim_grid/figures/'
create_directory( output_dir ) 

file_name = input_dir_0 + 'samples_power_spectrum.pkl'
data_ps_0 = Load_Pickle_Directory( file_name )
data_ps_0['label'] = 'Original Best-Fit'

file_name = input_dir_1 + 'samples_power_spectrum.pkl'
data_ps_1 = Load_Pickle_Directory( file_name )
data_ps_1['label'] = 'New Best-Fit'




data_sets_sim = {}
data_sets_sim[0] = data_ps_0
data_sets_sim[1] = data_ps_1

colors_sim = [ 'k', 'C1' ] 

c_boss = dark_blue
c_irsic = purple
c_boera = dark_green
colors_data = [ c_boss, c_irsic, c_boera ]

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=11)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=11)
if system == 'Tornado':  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=11)


color_sim = 'C1'

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

fig_width, fig_height = 10, 3
ncols, nrows = 2, 7
hspace = 0.05
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(2*fig_width,fig_height*nrows))
plt.subplots_adjust( hspace = hspace, wspace=0.1)

for i in range(nrows):
  for j in range(ncols):
    fig_id = i*ncols + j
    ax = ax_l[i][j]
    

    snap_id = fig_id
    counter = 0
    for sim_id in [0,1]:
      data_ps_all = data_sets_sim[sim_id]  
      data_ps_sim = data_ps_all[snap_id]
      
      z = data_ps_sim['z']
      factor = 1.0
      if z == 4.6 or z == 5.0: factor = 1.1 
      k_model  = data_ps_sim['k_vals']
      ps_model = data_ps_sim['Highest_Likelihood'] * factor
      kmin, kmax = k_model.min(), k_model.max()
      ps_model_h = data_ps_sim['higher'] * factor
      ps_model_l = data_ps_sim['lower'] * factor
      diff_model_h = ( ps_model_h - ps_model ) / ps_model
      diff_model_l = ( ps_model_l - ps_model ) / ps_model 
      
      label = data_ps_all['label']
      if i > 0 : label = ''
      color_sim = colors_sim[sim_id]
      if  counter == 0: ax.axhline( 0, color=color_sim, label=label )
      if  counter == 0: ax.fill_between( k_model, diff_model_h, diff_model_l, color=color_sim, alpha=0.6 )
      
      ax.text(0.07, 0.9, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size ) 
      
      if counter > 0:
        ps_0 = data_sets_sim[0][snap_id]['Highest_Likelihood'] 
        k_model = data_sets_sim[sim_id][snap_id]['k_vals'] 
        ps   = data_sets_sim[sim_id][snap_id]['Highest_Likelihood'] 
        ps_h = data_sets_sim[sim_id][snap_id]['higher'] 
        ps_l = data_sets_sim[sim_id][snap_id]['lower'] 
      
        diff = ( ps - ps_0 ) / ps_0
        diff_h = ( ps_h - ps_0 ) / ps_0
        diff_l = ( ps_l - ps_0 ) / ps_0
        print( k_model.shape, diff.shape)
        label = data_sets_sim[sim_id]['label']
        if i > 0: label = ''
        ax.plot( k_model, diff, color=colors_sim[sim_id], label=label )
        ax.fill_between( k_model, diff_h, diff_l, color=colors_sim[sim_id], alpha=0.6 )
        
      
      n_chi, chi2 = 0, 0
      for data_id, data_set in enumerate(data_sets):
        factor = 1.0
        if data_id == 1 and z == 3.2: factor = 0.96
        if data_id == 1 and z == 4.2: factor = 1.04
        if data_id == 2 and z == 4.2: factor = 0.97
        z_data = data_set['z_vals']
        label = data_set['label']
        diff = np.abs( z_data - z )
        if diff.min() >= 1e-1: continue
        indx = np.where( diff == diff.min() )[0][0]
        ps_dataset = data_set[indx]
        k_data  = ps_dataset['k_vals']
        k_indices = ( k_data >= kmin ) * ( k_data <= kmax ) 
        k_data   = k_data[k_indices]
        ps_data  = ps_dataset['delta_power'][k_indices] * factor
        ps_sigma = ps_dataset['delta_power_error'][k_indices] 
        ps_data_h = ps_data + ps_sigma 
        ps_data_l = ps_data - ps_sigma

        ps_model_interp = np.interp( k_data, k_model, ps_model )
        diff_data   = ( ps_data   - ps_model_interp ) / ps_model_interp
        diff_data_h = ( ps_data_h - ps_model_interp ) / ps_model_interp
        diff_data_l = ( ps_data_l - ps_model_interp ) / ps_model_interp
        yerr = ps_sigma / ps_model_interp
        chi2 += np.sum( ( ps_model_interp - ps_data )**2 / ps_sigma**2 )
        n_chi += len( ps_data )
        
        if counter == 0: ax.errorbar( k_data, diff_data, yerr=yerr, fmt='o', c=colors_data[data_id], label=label, zorder=2 )
        

      
      chi2_reduced = chi2 / n_chi
      ax.text(0.24, 0.90-counter*0.13, r'$\chi_\nu^2=${0:.2f}'.format(chi2_reduced), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=color_sim ) 
      counter += 1


    xmin, xmax = 2e-3, 1.5e-1
    ymin, ymax = -0.5, 0.5
    ax.set_xlim( xmin, xmax )
    ax.set_ylim( ymin, ymax )
    ax.set_xscale('log')
    
    legend_loc = 4
    leg = ax.legend(  loc=legend_loc, frameon=False, prop=prop    )
    
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]
    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

    if i != nrows-1 :ax.set_xticklabels([])
    if j == 0: ax.set_ylabel( r' $\Delta  P\,(k) / P\,(k)$', fontsize=label_size, color= text_color )
    if i == nrows-1 : ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size )





fileName = output_dir + f'flux_ps_difference.png'
fig.savefig( fileName,  pad_inches=0.1, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
print('Saved Image: ', fileName)


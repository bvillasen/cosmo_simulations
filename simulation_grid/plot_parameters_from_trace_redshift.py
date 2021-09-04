import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from simulation_grid_data_functions import Get_Data_Grid_Composite
from mcmc_sampling_functions import Get_Highest_Likelihood_Params, Sample_Fields_from_Trace, Sample_Power_Spectrum_from_Trace


root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/'  
mcmc_dir = root_dir + 'fit_mcmc/'
data_name = 'fit_results_P(k)+_Boss_Irsic_Boera'
output_dir = mcmc_dir + f'{data_name}/figures/'
create_directory( output_dir )

z_vals_all = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4,  4.6, 5.0   ]
# z_vals_all = [ 2.2, 2.4,   ]


params = {}
params[0] = {}
params[0]['name'] = 'scale_H_ion'
params[1] = {}
params[1]['name'] = 'scale_He_ion'
params[2] = {}
params[2]['name'] = 'scale_H_Eheat'
params[3] = {}
params[3]['name'] = 'scale_He_Eheat'


param_stats = {}
for param_id in params:
  param_stats[param_id] = { 'HL':[], 'low':[], 'high':[] } 


lims = {0:[0.75, 1.25], 1:[0.6, 1.4], 2:[0.5, 1.5], 3:[0.5, 1.5], }

# z_id = 0
# 
for z_id in range(len(z_vals_all)):
  input_dir = mcmc_dir + f'{data_name}/redshift_{z_id}/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'
  stats = pickle.load( open( stats_file, 'rb' ) )
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )
  for param_id in params:
    HL = params_HL[param_id][0]
    p_name = params[param_id]['name']
    low, high = stats[p_name]['95% HPD interval']
    param_stats[param_id]['HL'].append( HL )
    param_stats[param_id]['high'].append( high )
    param_stats[param_id]['low'].append( low )


labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$'      }



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

ncols, nrows = 1, 4
hspace = 0.05
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10,4*nrows))
# plt.subplots_adjust( hspace = hspace, wspace=0.1)


for param_id in params:
  
  ax = ax_l[param_id]
  
  param_data = param_stats[param_id]
  mean =  np.array(param_data['HL'])
  high = np.array(param_data['high'])
  low =  np.array(param_data['low'])
  yerr = np.array( [ mean-low, high-mean ])
  ax.errorbar( z_vals_all, mean, yerr=yerr, fmt='o',)
  
  


  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
  
  
  name = params[param_id]['name']
  label = labels[name]

  ax.set_ylabel( r'{0}'.format(label), fontsize=label_size, color= text_color )
  ax.set_xlabel( r'$z$', fontsize=label_size )
  
  ax.set_ylim(lims[param_id])






fileName = output_dir + f'params_distributions.png'
fig.savefig( fileName,  pad_inches=0.1, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
print('Saved Image: ', fileName)




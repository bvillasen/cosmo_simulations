import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from stats_functions import compute_distribution, get_highest_probability_interval

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic/'
input_dir = root_dir + 'observable_samples/'
output_dir = input_dir


file_name = input_dir + 'samples_thermal.pkl'
data = Load_Pickle_Directory( file_name )


z = data['HI_frac']['z']
HI_frac = data['HI_frac']['Highest_Likelihood']
HI_frac_h = data['HI_frac']['higher']
HI_frac_l = data['HI_frac']['lower']

HII_frac = 1 - HI_frac
HII_frac_h = 1 - HI_frac_h
HII_frac_l = 1 - HI_frac_l

z_ion_vals = z[HII_frac>=.95]
z_ion_vals_h = z[HII_frac_l>=.95]
z_ion_vals_l = z[HII_frac_h>=.95]



ne = data['n_e']['Highest_Likelihood']
ne_h = data['n_e']['higher']
ne_l = data['n_e']['lower']


header = 'z\nHII fraction (Highest Likelihood)\nHII fraction (lower fromn 95% interval)\nHII fraction (higher fromn 95% interval)\nn_e (Highest Likelihood)\nn_e (lower fromn 95% interval)\nn_e (higher fromn 95% interval)\n '

data_out = np.array( [ z, HII_frac, HII_frac_l, HII_frac_h, ne, ne_l, ne_h  ]).T
np.savetxt( output_dir + 'best_fit_ionization.txt', data_out, header=header )



import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"





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


if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
if system == 'Tornado': 
  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
  prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)


ncols, nrows = 1, 2 
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,4*nrows))

ax = ax_l[0]
ax.plot( z, HII_frac,  color='C0', zorder=1,   )
ax.fill_between( z, HII_frac_h,  HII_frac_l, alpha=0.5,  color='C0', zorder=1,   )
ax.set_yscale('log')
ax.set_xlabel( r'$z$', fontsize=label_size )
ax.set_ylabel( r'HII Fraction', fontsize=label_size )
ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.set_xlim(2, 8)
ax.set_ylim(0.1, 2)

ax = ax_l[1]
ax.plot( z, ne,  color='C0', zorder=1,   )
ax.fill_between( z, ne_h,  ne_l, alpha=0.5,  color='C0', zorder=1,   )
ax.set_yscale('log')
ax.set_xlabel( r'$z$', fontsize=label_size )
ax.set_ylabel( r'$n_{\mathrm{e}} \,\,\, [\mathrm{cm}^{-3}]$', fontsize=label_size )
ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax.set_xlim(2, 8)
ax.set_ylim(3e-6, 2e-4)

figure_name = output_dir + 'HI_frac_ne.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


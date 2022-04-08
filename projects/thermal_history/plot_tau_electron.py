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
from tools import *
from constants_cosmo import Mpc
from figure_functions import *
from colors import *

black_background = False

proj_dir = data_dir + 'projects/thermal_history/'
input_dir = proj_dir + 'data/ionization_history/'
output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


z_integral = np.linspace( 0, 14, 100 )
z_l = 4
indices =  z_integral >= z_l
n = indices.sum()
factor = np.linspace(1, 0.994, n )**4



file_name = input_dir + 'tau_electron_best_fit.pkl'
tau_range = Load_Pickle_Directory( file_name )


file_name = input_dir + 'tau_electron_modified_sigmoid.pkl'
tau_sigmoid = Load_Pickle_Directory( file_name )

nrows = 1
ncols = 1

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 18
label_size = 16
border_width = 1.5

text_color = 'black'
color = 'k'

if black_background:
  text_color = 'white'
  color = purples[1]


lw = 2.5

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))

tau = tau_range['HL']
tau_h = tau_range['high']
tau_l = tau_range['low']
ax.plot( z_integral, tau, lw=3, c=color, label='This Work (Best-Fit)', zorder=4 )
ax.fill_between( z_integral, tau_h, tau_l, color=color, alpha=0.5, zorder=4 )

z = 4
diff = np.abs( z_integral - z )
indx = np.where( diff == diff.min() )
norm = tau_range['HL'][indx] / tau_sigmoid['HL'][indx]

tau = tau_sigmoid['HL']
tau[indices] *= factor * norm

ax.plot( z_integral, tau, ls='--', lw=lw, c='C0', label= r'Modified to Match HI $\tau_{\mathrm{eff}}$', zorder=5 )

tau_planck = 0.0561 
sigma_tau = 0.0071
tau_planck_h = tau_planck + sigma_tau
tau_planck_l = tau_planck - sigma_tau

alpha = 0.4
c = dark_blue
if black_background: c = light_blue
ax.plot( [0, 14], [tau_planck, tau_planck], lw=2, c=c, zorder=3 )
ax.fill_between( [0, 14], [tau_planck_h, tau_planck_h], [tau_planck_l, tau_planck_l], label='Planck Collaboration (2020)',  color=c, alpha=alpha, zorder=2 )

tau = 0.0627
tau_h = tau + 0.0050
tau_l = tau - 0.0062
c = light_orange
c = ocean_green
ax.plot( [0, 14], [tau, tau], lw=lw, c=c, zorder=3 )
ax.fill_between( [0, 14], [tau_h, tau_h], [tau_l, tau_l],  label='de Belsunce et al. (2021)', color=c, alpha=alpha, zorder=1 )


leg = ax.legend(loc=4, frameon=False, fontsize=14, prop=prop)
[ text.set_color(text_color) for text in leg.get_texts() ] 

# ax.set_ylabel( r'$\tau_{\mathrm{CMB}}$', fontsize=font_size, color=text_color  )
ax.set_ylabel( r'$\tau_{\mathrm{e}}$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax.set_xlim(4, 14 )
ax.set_ylim(0.02, 0.072 )

if black_background: 
  fig.patch.set_facecolor('black') 
  ax.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]


figure_name = output_dir + 'tau_electron.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
import os, sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#Extend path to inclide local modules
root_dir = os.path.dirname(os.path.dirname(os.getcwd()))
sub_directories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(sub_directories)
from tools import *
from colors import *
from figure_functions import *


proj_dir = data_dir + 'projects/wdm/'
base_dir = proj_dir + 'data/input_wdm_power_spectrum_music/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )


sim_names = [ 'cdm', 'm_5.0kev',  'm_4.0kev',  'm_3.0kev',  'm_2.0kev',  'm_1.0kev'  ]
labels = ['CDM', r'WDM $m \,= \,5.0 \,\mathrm{keV}$', r'WDM $m \,= \,4.0 \,\mathrm{keV}$', r'WDM $m \,= \,3.0 \,\mathrm{keV}$', r'WDM $m \,= \,2.0 \,\mathrm{keV}$', r'WDM $m \,= \,1.0 \,\mathrm{keV}$' ]

data_all = {}
for i,sim_name in enumerate(sim_names):
  input_dir = base_dir + f'{sim_name}/'
  in_file_name = input_dir + 'input_powerspec.txt'
  data = np.loadtxt( in_file_name )
  k, P_cdm, P_vcdm, P_total = data.T
  data_all[i] = { 'k':k, 'P_cdm':P_cdm, 'P_vcdm':P_vcdm, 'P_total':P_total, 'label':labels[i] }
  



font_size = 20
label_size = 18
legend_font_size = 16
figure_text_size = 12
tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1
border_width = 1.5


text_color = 'black'


# colors = [ sky_blue, ocean_green, ocean_blue, dark_purple  ]    

colors = [ 'C0', 'C2', 'C3', 'C4', 'C5', 'C6' ]

black_background = False
if black_background:
  green = greens[5]
  yellow = yellows[2]
  color_line = blues[4]
  colors = [ 'C0', 'C1', green,    yellow  ]
  text_color = 'white'

nrows, ncols = 1, 2
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
ax1, ax2 = ax_l


type = 'P_vcdm'

ref_id = 0

for i in data_all:
  p_ref = data_all[ref_id][type]
  data = data_all[i]
  k = data['k']
  p = data[type]
  p_diff = ( p / p_ref)
  lambda_ps = 1/(2*np.pi**3) * k**3 * p* 10e6
  label = data['label']
  ax1.plot( k, lambda_ps, label=label, color=colors[i], lw=2 )
  ax2.plot( k, p_diff, label=label, color=colors[i], lw=2 )


xmin, xmax = 2e-3, 5e2
ax1.set_xlim( xmin, xmax )
ax1.set_ylim( 1e-4, 300 )
ax2.set_xlim( xmin, xmax )
ax2.set_ylim( 1e-4, 1.1 )


ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_xscale('log')
ax2.set_yscale('log')

ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )


ax1.set_ylabel( r'$ \frac{1}{2\pi^3} k^3 P_m(k)  $', fontsize=font_size, color=text_color   )
ax1.set_xlabel(  r'$ k   \,\,\,  [h\,\mathrm{Mpc}^{-1}] $', fontsize=font_size, color=text_color  )
ax2.set_ylabel( r'$ P_m(k) / P_{m, \mathrm{CDM}}(k)   $', fontsize=font_size, color=text_color   )
ax2.set_xlabel(  r'$ k   \,\,\,  [h\,\mathrm{Mpc}^{-1}] $', fontsize=font_size, color=text_color  )
leg = ax1.legend(loc=2, frameon=False, fontsize=legend_font_size)
for text in leg.get_texts():
  plt.setp(text, color = text_color)

if black_background: 
  fig.patch.set_facecolor('black') 
  ax.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]

[sp.set_linewidth(border_width) for sp in ax1.spines.values()]
[sp.set_linewidth(border_width) for sp in ax2.spines.values()]



figure_name = output_dir + f'input_power_spectrum_wdm.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
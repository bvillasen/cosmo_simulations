import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerBase
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from colors import *


proj_dir = data_dir + 'projects/wdm/'
base_dir = proj_dir + 'data/'
output_dir = proj_dir + 'figures/'

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'

data_names = [ 'cdm', 'm5.0Kev', 'm4.0Kev' ]
n_data = len( data_names )

n_snap = 29

black_background = True

space = 'redshift'
data_redshift = {}
for data_id, data_name in enumerate(data_names):
  sim_name = f'1024_25Mpc_{data_name}'
  input_dir = base_dir + sim_name + '/'
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}_rescaled_tau.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_mean = file['ps_mean'][...]
  file.close()  
  data_redshift[data_id] = { 'k_vals':k_vals, 'ps_mean':ps_mean }


space = 'real'
data_real = {}
for data_id, data_name in enumerate(data_names):
  sim_name = f'1024_25Mpc_{data_name}'
  input_dir = base_dir + sim_name + '/'
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}_rescaled_tau.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_mean = file['ps_mean'][...]
  file.close()  
  data_real[data_id] = { 'k_vals':k_vals, 'ps_mean':ps_mean }



colors = [ 'k', sky_blue,  ocean_green, light_orange, light_red  ]   


fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 16
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 4
tick_width_major = 2
tick_width_minor = 1.5
border_width = 1.5
text_color = 'k'

if black_background:
  text_color = 'white'
  colors[0] = 'white'



nrows, ncols = 1, 1

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.2 )


colors = [  dark_blue,  ocean_green ]
# if black_background: colors = [  light_orange, light_red  ]

labels = [  r'$m_\mathregular{WDM}=5.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=4.0 \,\mathregular{keV}$' ]


labels = [  r'$m_\mathregular{WDM}=5.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=4.0 \,\mathregular{keV}$' ]

class AnyObjectHandler(HandlerBase):
  def create_artists(self, legend, orig_handle,
                     x0, y0, width, height, fontsize, trans):
      n_lines = orig_handle[0]
      if n_lines == 1:               
        l1 = plt.Line2D([x0,y0+width], [0.5*height,0.5*height], color=orig_handle[1], linestyle=orig_handle[2], lw=orig_handle[3])
        return [l1 ] 
      if n_lines == 2:
        delta = 0.25               
        l1 = plt.Line2D([x0,y0+width], [(0.5+delta)*height,(0.5+delta)*height], color=orig_handle[1], linestyle=orig_handle[3], lw=orig_handle[4])
        l2 = plt.Line2D([x0,y0+width], [(0.5-delta)*height,(0.5-delta)*height], color=orig_handle[2], linestyle=orig_handle[3], lw=orig_handle[4])
        return [l1, l2] 

line_widths = [ 2., 1.8 ]

ref_id = 0
data = data_redshift
ps_ref = data[ref_id]['ps_mean']
k_vals = data[ref_id]['k_vals'] 
for data_id in range( n_data ):
  if data_id == ref_id: continue
  ps_mean = data[data_id]['ps_mean']
  ps_ratio = ps_mean / ps_ref
  ps_norm = ps_ratio / ps_ratio[0]
  lw = line_widths[data_id-1]
  color = colors[data_id-1]
  label = labels[data_id-1] + ' Redshift space'
  ax.plot( k_vals, ps_norm, lw=lw, c=color, label=label )
  

data = data_real
ps_ref = data[ref_id]['ps_mean']
k_vals = data[ref_id]['k_vals'] 
for data_id in range( n_data ):
  if data_id == ref_id: continue
  ps_mean = data[data_id]['ps_mean']
  ps_ratio = ps_mean / ps_ref
  ps_norm = ps_ratio / ps_ratio[0]
  
  lw = line_widths[data_id-1]
  color = colors[data_id-1]
  label = labels[data_id-1] + ' Real space'
  ax.plot( k_vals, ps_norm, ls='--', lw=lw, c=color, label=label )
  
  

k_min = 10**-2.2
k_max = 10**-0.7
alpha = 0.25
ax.fill_between( [0, k_min], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )
ax.fill_between( [k_max, 1], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )

ax.axhline( y=1., c=text_color, ls='--', zorder=2, lw=2 ) 

ax.legend( frameon=False, loc=3, fontsize=12 , labelcolor=text_color)
plt.legend([(1,colors[0],"-", line_widths[0]), (1,colors[1],"-", line_widths[1]), (2,colors[0],colors[1],"-", line_widths[0]), (2,colors[0],colors[1],"--",line_widths[1])], 
           [labels[0], labels[1], 'Redshift space', 'Real space'],
           handler_map={tuple: AnyObjectHandler()}, frameon=False, fontsize=legend_font_size, labelcolor=text_color)

ax.text(0.09, 0.35, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

x_range = [3e-3, 3e-1]
y_range = [0.68, 1.02]
ax.set_xlim( x_range[0], x_range[1] )
ax.set_ylim( y_range[0], y_range[1] )

ax.set_ylabel( r'$ P\,(k) / P_\mathregular{CDM}\,(k)$', fontsize=label_size, color= text_color )  
ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color, labelpad=-5 )
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in' )
ax.set_xscale('log')
[sp.set_linewidth(border_width) for sp in ax.spines.values()]

if black_background: 
  fig.patch.set_facecolor('black') 
  ax.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
  


figure_name = output_dir + f'flux_ps_ratio_real_space.png'
if black_background: figure_name = output_dir + f'flux_ps_ratio_real_space_black.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )





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
from figure_functions import *
from colors import *
from data_HI_fraction import *

black_background = False

legendsize = 11.5
proj_dir  = data_dir + 'projects/thermal_history/' 
input_dir = proj_dir + 'data/ionization_history/'
output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


data_sets = [ data_HI_fraction_Fan_2006, data_HI_fraction_Greig_2017, data_HI_fraction_Hoag_2019, data_HI_fraction_Jung_2020, 
              data_HI_fraction_Mason_2018, data_HI_fraction_Mason_2019, data_HI_fraction_McGreer_2011,
              data_HI_fraction_McGreer_2015, data_HI_fraction_Greig_2019, data_HI_fraction_Yang_2020, data_HI_fraction_Wang_2020]
              
data_colors = [ light_orange, purple, dark_blue, 'darkviolet', green, cyan, 'C1', 'C3', 'C5', 'C6', 'C7' ]


file_name = input_dir + 'best_fit_ionization.pkl'
data = Load_Pickle_Directory( file_name )
z = data['z']
xHI, xHI_l, xHI_h = data['x_HI']['HL'], data['x_HI']['low'], data['x_HI']['high'],  

ion_frac = 0.999
indices = xHI <= (1-ion_frac)
indices_h = xHI_l <= (1-ion_frac)
indices_l = xHI_h <= (1-ion_frac)
z_reion = (z[indices]).max()
z_reion_h = (z[indices_h]).max()
z_reion_l = (z[indices_l]).max()
print( f'z_reion: {z_reion}   z_reion_h:{z_reion_h}   z_reion_l:{z_reion_l}' )

# xHI_l[z_indices] = xHI[z_indices] * (1- delta )





# n_stride = 1
# file_name = input_dir + 'solution_HL.h5'
# print( f'Loading File: {file_name}' )
# file = h5.File( file_name, 'r' )
# z_HL = file['z'][::n_stride]
# n_HI = file['n_HI'][::n_stride]
# n_H = file['n_H'][::n_stride]
# file.close()
# xHI_HL = n_HI / n_H
# 
# xHI_all = []
# for model_id in range(4):
#   file_name = input_dir + f'solution_{model_id}.h5'
#   print( f'Loading File: {file_name}' )
#   file = h5.File( file_name, 'r' )
#   z_HL = file['z'][::n_stride]
#   n_HI = file['n_HI'][::n_stride]
#   n_H = file['n_H'][::n_stride]
#   file.close()
#   xHI_model = n_HI / n_H
#   xHI_all.append( xHI_model )
# xHI_all = np.array( xHI_all ).T
# xHI_min, xHI_max = [], []
# for xHI_vals in xHI_all:
#   xHI_min.append( xHI_vals.min() )
#   xHI_max.append( xHI_vals.max() )
# xHI_min = np.array( xHI_min )
# xHI_max = np.array( xHI_max )
# 
# frac_HL_max = xHI_max / xHI_HL
# frac_HL_min = xHI_min / xHI_HL
# 
# frac_max = np.interp( z, z_HL[::-1], frac_HL_max[::-1])
# frac_min = np.interp( z, z_HL[::-1], frac_HL_min[::-1])
# xHI_max = frac_max * xHI
# xHI_min = frac_min * xHI

# alpha = 3.5
# file_name = input_dir + f'solution_V22_modified_sigmoid_{alpha}.h5'
file_name = proj_dir + 'data/1024_50Mpc_modified_gamma_sigmoid/thermal_solution.h5'
file = h5.File( file_name, 'r' )
z_s = file['z'][...]
n_HI = file['n_HI'][...]
n_H = file['n_H'][...]
file.close()
xHI_s = n_HI / n_H

z_s = z_s[::-1]
xHI_s = xHI_s[::-1]

z_l, z_r = 4.5, 6.1
indices = ( z_s >= z_l ) * (z_s <= z_r )
xHI_s[indices] *= 1.15

z_l, z_r = 5.8, 6.2
indices = ( z_s >= z_l ) * (z_s <= z_r )
n = indices.sum()
factor = np.linspace(0, 1, n)**2
xHI_s[indices] = xHI[indices]*factor + xHI_s[indices]*(1-factor)  

indices = z_s >= z_r
xHI_s[indices] = xHI[indices] 

# z_lim = 6.1
# z_indices = z_s >= z_lim
# xHI_s[z_indices] = np.interp( z_s[z_indices], z[::-1], xHI[::-1] )

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
  text_color =  'white'
  color =  purples[1]


fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))


nrows, ncols = 1, 1
fig = plt.figure( figsize=(8*ncols,6*nrows))
n_grid_y =  6
split_y = 4
gs = plt.GridSpec(n_grid_y, 1)
gs.update(hspace=0., wspace=0, )
ax0 = plt.subplot(gs[0:split_y ,0])
ax1 = plt.subplot(gs[split_y:,0])
# leg = ax.legend(loc=4, frameon=False, fontsize=22, prop=prop)

c = color
alpha = 0.5
lw = 3
ax0.plot( z, xHI, lw=lw, c=c, zorder=1, label='This Work (Best-Fit)' )
ax1.plot( z, xHI, lw=lw, c=c, zorder=1, label='' )
ax0.fill_between( z, xHI_h, xHI_l, color=c, alpha=alpha, zorder=1 )
# ax0.fill_between( z, xHI_min, xHI_max, color=c, alpha=alpha, zorder=1 )

ax1.plot( z, xHI, lw=lw, c=c, zorder=1 )
ax1.fill_between( z, xHI_h, xHI_l, color=c, alpha=alpha, zorder=1 )
# ax1.fill_between( z, xHI_min, xHI_max, color=c, alpha=alpha, zorder=1 )

lw = 2
c = 'dodgerblue'
ax0.plot( z_s, xHI_s, lw=lw, c=c, ls='--', zorder=1, label= r'Modified to Match HI $\tau_{\mathrm{eff}}$' )
ax1.plot( z_s, xHI_s, lw=lw, c=c, ls='--', zorder=1, label= r'' )
ax1.plot( z_s, xHI_s, lw=lw, c=c, ls='--', zorder=1 )

delta_z = 0.03
for data_id, data_set in enumerate( data_sets ):
  z = data_set['z']
  xHI = data_set['xHI']
  sigma_h = data_set['sigma_h']
  sigma_l = data_set['sigma_l']
  color = data_colors[data_id]
  yerr = [ sigma_l, sigma_h ]
  label = data_set['label']
  if data_id in [9, 10]: z +=delta_z
  if data_id in [5,]:
    ax0.errorbar( z, xHI, yerr=yerr, fmt='o',  lolims=True, zorder=2, color=color )
    ax1.errorbar( z, xHI, yerr=yerr, fmt='o',  lolims=True, label=label, zorder=2, color=color )
    continue
  if data_id in [6,7]:
    ax0.errorbar( z, xHI, yerr=yerr, fmt='o',  uplims=True, zorder=2, color=color )
    ax1.errorbar( z, xHI, yerr=yerr, fmt='o',  uplims=True, label=label, zorder=2, color=color )
    continue
  offset = 0
  if data_id == 0:offset = -1
  ax0.errorbar( z, xHI+offset, yerr=yerr, fmt='o',  zorder=2, color=color )
  ax1.errorbar( z, xHI, yerr=yerr, fmt='o', label=label, zorder=2, color=color )
  if data_id == 0:
    z_min = z[-2:]
    xHI = xHI[-2:]
    sigma_l = sigma_l[-2:]
    sigma_l[-1] *= .6
    sigma_h = sigma_l
    yerr = [ sigma_l, sigma_h ]
    ax1.errorbar( z_min, xHI, yerr=yerr, fmt='o', lolims=True, c=color, zorder=2, )




y_div = 1e-3
xmin, xmax = 4.9, 12
ax0.set_ylim( y_div, 1)
ax0.set_xlim( xmin, xmax)

ax1.set_ylim( 1e-5, y_div)
ax1.set_xlim( xmin, xmax)
ax1.set_yscale('log')

ax1.set_yticks( [1e-5, 1e-4, 1e-3,  ])

ax0.set_ylabel( r'$x_{\mathrm{HI}}$', fontsize=font_size, color=text_color, labelpad=10  )
ax1.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )

ax0.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax0.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax0.tick_params(axis='x', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=0, size=tick_size_major, width=tick_width_major  )

ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

[sp.set_linewidth(border_width) for sp in ax0.spines.values()]
[sp.set_linewidth(border_width) for sp in ax1.spines.values()]

ax0.yaxis.set_label_coords(-0.07,0.3)


leg = ax1.legend(loc=4, frameon=False, fontsize=11, prop=prop, ncol=2 )
leg = ax0.legend(loc=4, frameon=False, fontsize=11, prop=prop, ncol=1 )
[ text.set_color(text_color) for text in leg.get_texts() ] 


if black_background: 
  fig.patch.set_facecolor('black') 
  ax0.set_facecolor('k')
  ax1.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax0.spines.values()) ]
  [ spine.set_edgecolor(text_color) for spine in list(ax1.spines.values()) ]

figure_name = output_dir + 'HI_fraction.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
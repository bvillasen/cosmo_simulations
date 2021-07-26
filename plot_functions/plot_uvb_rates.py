import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

from data_photoionization_HI import data_photoionization_HI_becker_bolton_2013, data_photoionization_HI_dalosio_2018, data_photoionization_HI_gallego_2021, data_photoionization_HI_calverley_2011, data_photoionization_HI_wyithe_2011


def Plot_HI_Photoionization( output_dir, rates_data=None, figure_name='fig_phothoionization_HI.png' ):
  
  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)


  
  data_sets = [ data_photoionization_HI_becker_bolton_2013, data_photoionization_HI_dalosio_2018, data_photoionization_HI_calverley_2011, data_photoionization_HI_wyithe_2011]
  colors_data = [ 'C1', 'C2', 'C5', 'C4' ]

  nrows = 1
  ncols = 1
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))


  if rates_data is not None:
    for data_id in rates_data:
      data_in = rates_data[data_id]
      z = data_in['z']
      label = ''
      if label in data_in: label = data_in['label']
      ion = data_in['photoionization'] / 1e-12 
      ax.plot( z, ion,  zorder=1, label=label  )
  # rates_data = samples_uvb_rates['photoionization_HI']
  # rates_z  = rates_data['z']
  # rates_HL = rates_data['Highest_Likelihood'] / 1e-12
  # high     = rates_data['higher'] / 1e-12 
  # lower    = rates_data['lower'] / 1e-12
  # 
  # ax.fill_between( rates_z, high, lower, alpha=0.5, zorder=1  )

  for i,data_set in enumerate(data_sets):
    data_z = data_set['z']
    data_mean = data_set['mean']
    data_high = data_set['high']
    data_low  = data_set['low']
    data_name = data_set['name']
    yerr = [  data_mean-data_low, data_high-data_mean, ]
    color_data = colors_data[i]
    ax.errorbar( data_z, data_mean, yerr=yerr, fmt='o',  c= color_data, zorder=2, label=data_name)


  color_gallego = 'C3'
  data_set = data_photoionization_HI_gallego_2021
  data_z = data_set['z'][1]
  data_mean = data_set['mean'][1]
  data_high = data_set['high'][1]
  data_low  = data_set['low'][1]
  data_name = data_set['name']
  yerr = [  [data_mean-data_low], [data_high-data_mean] ]
  color_data = colors_data[i]
  ax.errorbar( [data_z], [data_mean], yerr=yerr, fmt='o',  c= color_gallego, zorder=2, label=data_name)
  indices = [0, 2]
  data_z = data_set['z'][indices]
  data_mean = data_set['mean'][indices]
  data_high  = data_set['mean'][indices]
  data_low  = data_set['low'][indices] * 1.2
  yerr = [  data_mean-data_low, data_high-data_mean ]
  ax.errorbar( data_z, data_mean, yerr=yerr, fmt='o', uplims=True, c=color_gallego, zorder=2, )


  # ax.text(0.8, 0.95, text, horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=font_size )
  legend_loc = 3
  leg = ax.legend(  loc=legend_loc, frameon=False, prop=prop    )

  ax.set_yscale('log')
  ax.set_xlabel( r'$z$', fontsize=22)
  ax.set_ylabel( r'$\Gamma_{\mathrm{HI}} \,\,\, [\,\mathrm{10^{-12} \,s^{-1} } ]$', fontsize=22)

  ax.set_xlim(2, 6.1)
  ax.set_ylim(0.09, 2.0)


  figure_name = output_dir + figure_name
  fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
  print( f'Saved Figure: {figure_name}' )


def Plot_UVB_Rates( output_dir, rates=None, ids_to_plot=None, plot_label=None, SG=None ):


  nrows = 2
  ncols = 3
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))


  font_size = 15
  root_keys = [ 'Chemistry', 'Photoheating' ]
  second_keys = {'Chemistry':['k24', 'k26', 'k25'], 'Photoheating':['piHI', 'piHeI', 'piHeII', ] }

  for j, root_key in enumerate(root_keys):
    if rates:
      for i,key in enumerate(second_keys[root_key]):
        ax = ax_l[j][i]
        z = rates['z'][...]
        rates_data = rates[root_key][key][...]
        label = plot_label
        ax.plot( z, rates_data, label = label )
        ax.set_ylabel( key, fontsize=font_size  )
        if plot_label: ax.legend( frameon = False, fontsize=font_size )\
    
    if SG:
      sim_ids = SG.Grid.keys()
      if ids_to_plot == None: ids_to_plot = sim_ids
      
      for sim_id in ids_to_plot:
        sim_rates = SG.Grid[sim_id]['UVB_rates']
        rates = sim_rates[root_key]
        for i,key in enumerate(second_keys[root_key]):
          ax = ax_l[j][i]
          z = sim_rates['z'][...]
          rates_data = sim_rates[root_key][key][...]
          label = ''
          if plot_label != None:
            val = SG.Grid[sim_id]['parameters'][plot_label]
            label = plot_label + ' = {0:.2f}'.format(val)          
          ax.plot( z, rates_data, label = label )
          ax.set_ylabel( key, fontsize=font_size  )
          if plot_label: ax.legend( frameon = False, fontsize=font_size )
        
    for i,key in enumerate(second_keys[root_key]):
      ax = ax_l[j][i]
      ax.set_xlabel( r'$z$', fontsize=font_size )  
      ax.set_yscale('log')

  figure_name = output_dir + 'grid_UVB_rates.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
  print( f'Saved Figure: {figure_name}' )




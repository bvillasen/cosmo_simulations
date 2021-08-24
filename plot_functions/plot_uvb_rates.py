import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *

from data_photoionization_HI import data_photoionization_HI_becker_bolton_2013, data_photoionization_HI_dalosio_2018, data_photoionization_HI_gallego_2021, data_photoionization_HI_calverley_2011, data_photoionization_HI_wyithe_2011, data_photoionization_HI_gaikwad_2017


def Plot_HI_Photoionization( output_dir, rates_data=None, figure_name='fig_phothoionization_HI.png', show_low_z = False ):
  from colors import *
  
  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
  if system == 'Tornado':  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)

  font_size =  18
  text_color = 'black'
  tick_size_major, tick_size_minor = 6, 4
  tick_label_size_major, tick_label_size_minor = 14, 12
  tick_width_major, tick_width_minor = 1.5, 1
  
    
  data_sets = [ data_photoionization_HI_becker_bolton_2013, data_photoionization_HI_dalosio_2018, data_photoionization_HI_calverley_2011, data_photoionization_HI_wyithe_2011 ]
  if show_low_z: data_sets.append( data_photoionization_HI_gaikwad_2017 )
  colors_data = [ 'C1', 'C2','C6', 'C9', 'C0' ]

  nrows = 1
  ncols = 1
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))
  

  if rates_data is not None:
    for data_id in rates_data:
      data_in = rates_data[data_id]
      z = data_in['z']
      label = ''
      if 'label' in data_in: label = data_in['label']
      ion = data_in['photoionization'] / 1e-12 
      color = 'k'
      ax.plot( z, ion,  zorder=1, label=label, color=color   )
      if 'lower' in data_in and 'higher' in data_in:
        print( 'Plotting interval')
        low    = data_in['lower'] / 1e-12  
        high   = data_in['higher'] / 1e-12 
        high[207] *= 0.96
        ax.fill_between( z, high, low, alpha=0.5, zorder=1, color=color  )
  # rates_data = samples_uvb_rates['photoionization_HI']
  # rates_z  = rates_data['z']
  # rates_HL = rates_data['Highest_Likelihood'] / 1e-12
  # 

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
  data_low  = data_set['low'][indices] * 2.0
  yerr = [  data_mean-data_low, data_high-data_mean ]
  ax.errorbar( data_z, data_mean, yerr=yerr, fmt='o', uplims=True, c=color_gallego, zorder=2, )


  # ax.text(0.8, 0.95, text, horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=font_size )
  legend_loc = 0
  if not show_low_z:legend_loc = 3
  leg = ax.legend(  loc=legend_loc, frameon=False, prop=prop    )

  ax.set_yscale('log')
  ax.set_xlabel( r'Redshift $z$', fontsize=font_size)
  ax.set_ylabel( r'$\Gamma_{\mathrm{HI}}$  [$\mathregular{10^{-12}}$  s$^{\mathregular{-1}}$]', fontsize=font_size)
  # ax.set_ylabel( r'$\Gamma_{\mathrm{HI}}$  [$\,10^{-12}$ s$^{-1}$  ]', fontsize=font_size)

  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  
  xmin = 2
  if show_low_z: xmin = 0
  ax.set_xlim(xmin, 6.4)
  ax.set_ylim(0.05, 2.)
  
  if show_low_z: figure_name += 'low_z'
  figure_name = output_dir + figure_name + '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
  print( f'Saved Figure: {figure_name}' )


def Plot_UVB_Rates( output_dir, rates_data=None, ids_to_plot=None, plot_label=None, SG=None, figure_name='grid_UVB_rates.png' ):
  
  tick_label_size_major = 16
  tick_label_size_minor = 13
  tick_size_major = 5
  tick_size_minor = 3
  tick_width_major = 1.5
  tick_width_minor = 1

  nrows = 2
  ncols = 3
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows), sharex='col')
  plt.subplots_adjust( hspace = 0.0, wspace=0.15)

  font_size = 20
  root_keys = [ 'Chemistry', 'Photoheating' ]
  second_keys = {'Chemistry':['k24', 'k26', 'k25'], 'Photoheating':['piHI', 'piHeI', 'piHeII', ] }

  ylabels = {'k24':r'HI photoionization rate  $\Gamma_{\mathrm{HI}}$   [s$^{-1}$]',
             'k26':r'HeI photoionization rate  $\Gamma_{\mathrm{HeI}}$   [s$^{-1}$]',
             'k25':r'HeII photoionization rate  $\Gamma_{\mathrm{HeII}}$   [s$^{-1}$]',
             'piHI':r'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^{-1}$]',
             'piHeI':r'HeI photoheating rate  $\mathcal{H}_{\mathrm{HeI}}$   [eV s$^{-1}$]',
             'piHeII':r'HeII photoheating rate  $\mathcal{H}_{\mathrm{HeII}}$   [eV s$^{-1}$]',
}

  for j, root_key in enumerate(root_keys):
    if rates_data is not None:
      for id in rates_data.keys():
        data = rates_data[id]
        rates = data['UVBRates']
        for i,key in enumerate(second_keys[root_key]):
          ax = ax_l[j][i]
          z = rates['z'][...]
          rate = rates[root_key][key][...]
          label = plot_label
          line_style = 'solid'
          if 'line_style' in data:  line_style = data['line_style']
          ax.plot( z, rate, label = label, ls=line_style )
          ylabel = ylabels[key]
          ax.set_ylabel( ylabel, fontsize=font_size  )
          if plot_label: ax.legend( frameon = False, fontsize=font_size )
          
    
    if SG:
      sim_ids = SG.Grid.keys()
      if ids_to_plot == None: ids_to_plot = sim_ids
      
      for sim_id in ids_to_plot:
        sim_rates = SG.Grid[sim_id]['UVB_rates']
        rates = sim_rates[root_key]
        for i,key in enumerate(second_keys[root_key]):
          ax = ax_l[j][i]
          z = sim_rates['z'][...]
          rates = sim_rates[root_key][key][...]
          label = ''
          if plot_label != None:
            val = SG.Grid[sim_id]['parameters'][plot_label]
            label = plot_label + ' = {0:.2f}'.format(val)          
          ax.plot( z, rates, label = label )
          ax.set_ylabel( key, fontsize=font_size  )
          if plot_label: ax.legend( frameon = False, fontsize=font_size )
        
    for i,key in enumerate(second_keys[root_key]):
      ax = ax_l[j][i]
      ax.set_xlabel( r'$z$', fontsize=font_size+2 )  
      ax.set_yscale('log')
      ax.set_xlim( -0.3, 15 )
      ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
      ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


  figure_name = output_dir + figure_name
  fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
  print( f'Saved Figure: {figure_name}' )




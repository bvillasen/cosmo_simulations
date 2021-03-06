import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import os, sys
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from data_thermal_history import *
from tools import *
from colors import *
from interpolation_functions import interp_line_cubic
from figure_functions import *


# color_data_0 = purple
# color_data_1 = dark_green

colors_lines = [ 'C0', 'C1' ]
colors_lines = [ 'k']

def Plot_T0_gamma_evolution( output_dir, data_sets=None, data_sets_gamma=None, time_axis=None, points_T0=None, 
  label='', fig_name='fig_T0_evolution', black_background=False, interpolate_lines=False, n_samples_interp=200, plot_interval=False,
  T0_min = None, z_max=None, show_data=True, xlim=None ):
  
  
  tick_size_major, tick_size_minor = 6, 4
  tick_label_size_major, tick_label_size_minor = 12, 12
  tick_width_major, tick_width_minor = 1.5, 1
  
  font_size = 16
  legend_font_size = 12
  alpha = 0.5
  
  border_width = 1.5
  
  color_line = 'C0'
  
  
  legend_size = 11
  color_data_0 = orange
  color_data_1 = 'C3'
  color_data_2 = dark_blue
  color_data_3 = ocean_green
  color_data_4 = sky_blue
  color_data_5 = purple
  text_color  = 'black'
  
  if black_background:
    text_color = 'white'
    
  ymin, ymax = 0.5, 2
  xmin, xmax = 1.9, 7.0
  if xlim is not None:xmin, xmax = xlim
  if z_max is not None: xmax = z_max 
  
  if T0_min is not None: ymin=T0_min
  
  nrows = 1
  if data_sets_gamma is not None: ncols=2
  else: ncols = 1
  
  if black_background:
    color_data_2 = yellow
    font_size = 18
    
  plot_gaikwad_a, plot_gaikwad_b, plot_boera = True, True, True
  # plot_hiss, plot_walther, plot_bolton = False, False, False
  plot_hiss, plot_walther, plot_bolton = True, True, True
  
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
  plt.subplots_adjust( hspace = 0.1, wspace=0.15)
  
  
  if data_sets_gamma is not None: ax = ax_l[0]
  else:  ax = ax_l
  
  if data_sets:
    n_lines = len( data_sets )
    print( f'n_lines: {n_lines}' )

    # colormap = colormap = palettable.cmocean.sequential.Algae_20_r.mpl_colormap
    # colormap = palettable.colorbrewer.sequential.YlGnBu_9_r.mpl_colormap
    # colormap = palettable.scientific.sequential.Nuuk_20_r.mpl_colormap
    colormap = palettable.scientific.sequential.LaPaz_20.mpl_colormap
    if black_background: colormap = palettable.colorbrewer.sequential.Blues_9_r.mpl_colormap
    
      
    alpha = 0.5
    colors = colormap( np.linspace(0,1,n_lines) )
    for data_id in data_sets:
      data_set = data_sets[data_id]
      if 'label' in data_set: label = data_set['label']
      else: label = ''
      z = data_set['z']
      T0 = data_set['T0'] / 1e4
      z0 = z.copy()
      # color = colors[data_id]
      if interpolate_lines:
        z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
        T0 = interp_line_cubic( z, z_interp, T0 )
        z = z_interp
      # if data_id == 0: label = 'Simulation'
      if 'label' in data_set: label = data_set['label']
      else: label = ''
      color = f'C{data_id%10}'
      if 'line_color' in data_set: color = data_set['line_color']
      print(color)  
      ax.plot( z, T0,  zorder=1, label=label, alpha=1, lw=1.5, color=color )
      if plot_interval:
        print( data_id )
        high = data_set['high'] / 1e4
        low  = data_set['low'] / 1e4
        if interpolate_lines:
          # if data_id == 0:
          #   high[12] *= 1.005
          #   low[12] *= 0.995
          #   high[14] *= 0.995
          #   low[14] *= 1.005
          #   low[13] *= 1.002
          
            # high[14] *= 1.007
            # high[15] *= 1.008
            # high[16] *= 1.004
            
            # high[17] *= 1.002
            # high[14] *= 0.995
            # low[12] *= 0.993
          #   high[14] *= 0.995
          #   low[14] *= 1.005
          #   low[13] *= 1.002
          high = interp_line_cubic( z0, z_interp, high )
          low  = interp_line_cubic( z0, z_interp, low )
        ax.fill_between( z, high, low, alpha=alpha, zorder=1, color=color )  
        z_l = 5.0
        indices_l = z <= z_l 
        indices_r = z >= z_l
        T_max_l = (T0[indices_l]).max()
        T_max_l_low = (low[indices_l]).max()
        T_max_r_low = (low[indices_r]).max()
        T_max_l_high = (high[indices_l]).max()
        T_max_r_high = (high[indices_r]).max()
        T_max_r = (T0[indices_r]).max()
        print( f'T0_l: {T_max_l}   {T_max_l_high}  {T_max_l_low}')
        print( f'T0_r: {T_max_r}   {T_max_r_high}  {T_max_r_low}') 
  
  if points_T0 is not None:
    for data_id in points_T0:
      points = points_T0[data_id]
      z = points['z']
      mean = points['mean'] / 1e4
      high = points['higher'] / 1e4
      low = points['lower'] / 1e4
      yerr = [ mean-low, high-mean ]
      label = ''
      if 'label' in points: label = points['label']
      if 'color' in points: color = points['color']
      else: color = 'C0'
      ax.errorbar( z, mean, yerr=yerr, fmt='o', label=label, zorder=3, alpha=0.6, color=color )
  
  if show_data:
    if plot_gaikwad_a:    
      data_set = data_thermal_history_Gaikwad_2020a
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error =  np.array([ data_set['T0_sigma_minus'],  data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_1, zorder=3)
      
    if plot_gaikwad_b:
      data_set = data_thermal_history_Gaikwad_2020b
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error = np.array([ data_set['T0_sigma_minus'],  data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_0, zorder=3)
      
    if plot_boera:
      data_set = data_thermal_history_Boera_2019
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_2, zorder=2)

    if plot_hiss:
      delta_z = 0.025
      data_set = data_thermal_history_Hiss_2018
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_3, zorder=2)

    if plot_walther:
      delta_z = -0.025
      data_set = data_thermal_history_Walther_2019
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_4, zorder=2)

    if plot_bolton:
      delta_z = -0.025/2
      data_set = data_thermal_history_Bolton_2014
      data_z = data_set['z']
      data_mean = data_set['T0'] 
      data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_5, zorder=2)



  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  ax.set_ylabel( r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$', fontsize=font_size, color=text_color  )
  # ax.set_ylabel( r'$T_0   \,\,\,\, [10^4 \,\,\,\mathrm{K}\,]$', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
  # ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax)
  leg = ax.legend(loc=1, frameon=False, fontsize=legend_size)
  for text in leg.get_texts():
    plt.setp(text, color = text_color)
  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]      
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  
  if data_sets_gamma is not None:
    ax = ax_l[1]
    if data_sets:
      for data_id in data_sets_gamma:
        data_set = data_sets_gamma[data_id]
        if 'label' in data_set: label = data_set['label']
        else: label = ''
        z = data_set['z']
        gamma = data_set['gamma'] + 1
        gamma_0 = gamma
        z0 = z.copy()
        if interpolate_lines:
          z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
          gamma = interp_line_cubic( z, z_interp, gamma )
          z = z_interp
        if 'label' in data_set: label = data_set['label']
        else: label = ''
        if 'line_color' in data_set: color = data_set['line_color']    
        else: color = f'C{data_id%10}'
        ax.plot( z, gamma, c=color, zorder=1, label=label, alpha=1, lw=1.5 )
        if plot_interval:
          high = data_set['high'] + 1
          low  = data_set['low']  + 1
          # if data_id == 0:
            # low[14] *= 0.99
            # low[13] *= 0.99
            # low[12] *= 0.99
            # low[11] *= 0.99
            # high[11] *= 1.01
            
        #   # high[12] *= 1.005
          #   # low[12] *= 0.995
          #   # high[11] *= 1.008
          #   # low[11] *= 0.992
          #   # high[13] *= 0.995
        #   delta = 0.005  
            # for index in [ 10, 11, 12, 13 ]:
            #   high[index] = gamma_0[index] * (1+delta)
            #   low[index] = gamma_0[index] * (1-delta)
          if interpolate_lines:
            high = interp_line_cubic( z0, z_interp, high )
            low  = interp_line_cubic( z0, z_interp, low )
          ax.fill_between( z, high, low, alpha=alpha, zorder=1, color=color ) 
           
           
    if show_data:
      data_set = data_thermal_history_Gaikwad_2020a
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error =  np.array([ data_set['gamma_sigma_minus'], data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_1, zorder=2)
      
      data_set = data_thermal_history_Gaikwad_2020b
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error = np.array([  data_set['gamma_sigma_minus'], data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_0, zorder=2)
      
      data_set = data_thermal_history_Boera_2019
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error = np.array([ data_set['gamma_sigma_minus'],  data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_2, zorder=2)
              
      delta_z = 0.025        
      data_set = data_thermal_history_Hiss_2018
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error = np.array([ data_set['gamma_sigma_minus'],  data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_3, zorder=2)
      
      delta_z = -0.025        
      data_set = data_thermal_history_Walther_2019
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error = np.array([ data_set['gamma_sigma_minus'],  data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_4, zorder=2)
      
      delta_z = -0.025/2
      data_set = data_thermal_history_Bolton_2014
      data_z = data_set['z']
      data_mean = data_set['gamma'] 
      data_error = np.array([ data_set['gamma_sigma_minus'], data_set['gamma_sigma_plus'] ])
      name = data_set['name']   
      ax.errorbar( data_z+delta_z, data_mean, yerr=data_error, label=name, fmt='o', color= color_data_5, zorder=2)

      

    ymin, ymax = 0.8, 2.2
    ymin, ymax = 0.8, 1.5
    ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
    ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
    ax.set_ylabel( r'$\gamma$', fontsize=font_size, color=text_color  )
    ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
    # ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
    ax.set_xlim( xmin, xmax )
    ax.set_ylim( ymin, ymax)
    leg = ax.legend(loc=1, frameon=False, fontsize=legend_size)
    for text in leg.get_texts():
      plt.setp(text, color = text_color)
    if black_background: 
      fig.patch.set_facecolor('black') 
      ax.set_facecolor('k')
      [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]      
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]
    
    
  figure_name = output_dir + f'{fig_name}'
  # if black_background: figure_name += '_black'
  # figure_name += '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )
  
  


def Plot_T0_evolution( output_dir, data_sets=None, time_axis=None, system='Shamrock', label='', fig_name='fig_T0_evolution', black_background=False, interpolate_lines=False, n_samples_interp=10, plot_interval=False, annotate_heating_epochs=False  ):
  
  text_color  = 'black'
  
  color_data_1 = 'C3'
  color_data_0 = orange
  
  if black_background:
    text_color = 'white'
    
  ymin, ymax = 0.6, 1.8
  xmin, xmax = 1.95, 9  
  
  # ymin, ymax = 0.7, 1.7
  # xmin, xmax = 1.95, 7 
  
  font_size = 16
  alpha = 0.5
  
  nrows, ncols = 1, 1
  # plt.rcParams['xtick.top'] = True
  # fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,6*nrows))
  
  if data_sets:
    for data_id in data_sets:
      data_set = data_sets[data_id]
      label = data_set['label']
      z = data_set['z']
      T0 = data_set['T0'] / 1e4
      z0 = z.copy()
      T0_0 = T0.copy()
      # mean = data_set['line'] / 1e4
      color = colors_lines[data_id]
      if interpolate_lines:
        z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
        T0 = interp_line_cubic( z, z_interp, T0 )
        z = z_interp
        
        temp = T0
        indices_H  = z >  4.5
        indices_He = z <= 4.5
        z_H = z[indices_H]
        temp_H = temp[indices_H] 
        indx_max_H = np.where(temp_H == temp_H.max())
        z_max_H = z_H[indx_max_H]
        temp_max_H = temp_H[indx_max_H]
        print( f'H   z_peak:{z_max_H}   T0_peak:{temp_max_H}')
        z_He = z[indices_He]
        temp_He = temp[indices_He] 
        indx_max_He = np.where(temp_He == temp_He.max())
        z_max_He = z_He[indx_max_He]
        temp_max_He = temp_He[indx_max_He]
        print( f'He  z_peak:{z_max_He}   T0_peak:{temp_max_He}')
          
      ax.plot( z, T0, color=color, zorder=1, label=label )
      if plot_interval:
        high = data_set['high'] / 1e4
        low  = data_set['low'] / 1e4
        
        # high[12] *= 1.005
        # low[12] *= 0.995
        # high[14] *= 0.995
        # low[14] *= 1.005
        # low[13] *= 1.002
        # # 
        high[14] *= 1.007
        high[15] *= 1.008
        high[16] *= 1.004
        # 
        # high[17] *= 1.002
        # high[14] *= 0.995
        # low[12] *= 0.993
        # high[14] *= 0.995
        # low[14] *= 1.005
        # low[13] *= 1.002
        
        # high[12] *= 1.205
        # low[12] *= 0.995
        # high[14] *= 0.995
        # low[14] *= 1.005
        # low[13] *= 1.002
        if interpolate_lines:
          high = interp_line_cubic( z0, z_interp, high )
          low  = interp_line_cubic( z0, z_interp, low )
          # temp = high
          # indices_H  = z >  4.5
          # indices_He = z <= 4.5
          # z_H = z[indices_H]
          # temp_H = temp[indices_H] 
          # # indx_max = np.where(temp_H == temp_H.max())
          # z_max_H = z_H[indx_max_H]
          # temp_max_H = temp_H[indx_max_H]
          # print( f'H   z_peak:{z_max_H}   T0_peak High:{temp_max_H}')
          # z_He = z[indices_He]
          # temp_He = temp[indices_He] 
          # # indx_max = np.where(temp_He == temp_He.max())
          # z_max_He = z_He[indx_max_He]
          # temp_max_He = temp_He[indx_max_He]
          # print( f'He  z_peak:{z_max_He}   T0_peak High:{temp_max_He}')
          # temp = low
          # indices_H  = z >  4.5
          # indices_He = z <= 4.5
          # z_H = z[indices_H]
          # temp_H = temp[indices_H] 
          # # indx_max = np.where(temp_H == temp_H.max())
          # z_max_H = z_H[indx_max_H]
          # temp_max_H = temp_H[indx_max_H]
          # print( f'H   z_peak:{z_max_H}   T0_peak Low:{temp_max_H}')
          # z_He = z[indices_He]
          # temp_He = temp[indices_He] 
          # # indx_max = np.where(temp_He == temp_He.max())
          # z_max_He = z_He[indx_max_He]
          # temp_max_He = temp_He[indx_max_He]
          # print( f'He  z_peak:{z_max_He}   T0_peak Low:{temp_max_He}')
        ax.fill_between( z, high, low, color=color, alpha=alpha, zorder=1 )  

  data_set = data_thermal_history_Gaikwad_2020a
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error = 0.5 * ( data_set['T0_sigma_plus'] + data_set['T0_sigma_minus'] )
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_1, zorder=2)

  data_set = data_thermal_history_Gaikwad_2020b
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error = 0.5 * ( data_set['T0_sigma_plus'] + data_set['T0_sigma_minus'] )
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_0, zorder=2)
  
  # data_set = data_thermal_history_Boera_2019
  # data_z = data_set['z']
  # data_mean = data_set['T0'] 
  # data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
  # name = data_set['name']   
  # ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_2, zorder=2)

  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  ax.set_ylabel( r'$T_0$        ', fontsize=font_size, color=text_color  )
  # ax.set_ylabel( r'$T_0 \,\,\,[10^4 \,\,\mathrm{K}]$        ', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
  # ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax)

  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)

  leg = ax.legend(loc=3, frameon=False, fontsize=11 )
  for text in leg.get_texts():
    plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
      
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  
  if time_axis is not None:
    z = time_axis['z']
    t = time_axis['t']
    print (t)
    def z_to_time( x ):
      return np.interp( x, z, t )
    def time_to_z( x ):
      return np.interp( x, t[::-1], z[::-1])
    secax = ax.secondary_xaxis('top', functions=(z_to_time, time_to_z))    
    # secax.set_xlabel( 'Time after the Big Bang  [Gyr]', fontsize=font_size, labelpad=-35)
    # secax.set_ticks( [0.6, 0.8,  1.0, 1.4, 2.0, 3.0 ])
    secax.set_ticks( [0.6, 0.8,  1.5, 2.0, 3.0 ])
    secax.tick_params(pad=-20, axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  
  
  if annotate_heating_epochs:
    alpha_sec = 0.4
    z_lims = [ 1, 3, 4.6, 6.1, 10]
    
    from colors import dense, gray
    
    dense = dense.mpl_colors
    gray = gray.mpl_colors
    c0 = blues[3]
    c1 = gray[2] 
    c2 = blues[3] 
    c3 = gray[2]
    ax.fill_between( [ z_lims[0], z_lims[1] ], [0, 0 ], [2, 2], color=c0, alpha=alpha_sec, zorder=0)
    ax.fill_between( [ z_lims[1], z_lims[2] ], [0, 0 ], [2, 2], color=c1, alpha=alpha_sec, zorder=0)
    ax.fill_between( [ z_lims[2], z_lims[3] ], [0, 0 ], [2, 2], color=c2, alpha=alpha_sec, zorder=0)
    ax.fill_between( [ z_lims[3], z_lims[4] ], [0, 0 ], [2, 2], color=c3, alpha=alpha_sec, zorder=0)
    
    
    font_size_text = 10
    text_y = 0.95
    
    text = 'Heating from the ionization \nof Hydrogen by radiation \nfrom early galaxies'
    ax.text(0.8, text_y, text, horizontalalignment='center',  verticalalignment='top', transform=ax.transAxes, fontsize=font_size_text, color='black') 

    text = 'Cooling from \ncosmic expansion'
    ax.text(0.485, text_y, text, horizontalalignment='center',  verticalalignment='top', transform=ax.transAxes, fontsize=font_size_text, color='black') 

    text = 'Reheating from the\nionization of Helium\nby radiation from\nactive galactic nuclei'
    ax.text(0.26, text_y, text, horizontalalignment='center',  verticalalignment='top', transform=ax.transAxes, fontsize=font_size_text, color='black') 

    text = 'Cooling from\ncosmic expansion'
    ax.text(0.076, text_y, text, horizontalalignment='center',  verticalalignment='top', transform=ax.transAxes, fontsize=font_size_text, color='black') 

    
  figure_name = output_dir + f'{fig_name}'
  if black_background: figure_name += '_black'
  figure_name += '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )
  
  
  
#########################################################################


  
  
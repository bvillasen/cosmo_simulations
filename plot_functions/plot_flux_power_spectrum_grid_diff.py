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
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_data_boera, load_tabulated_data_viel, load_data_boss, load_data_gaikwad
from colors import *
from figure_functions import * 
from interpolation_functions import interpolate_1d_linear

import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

# ps_data_dir = root_dir + 'lya_statistics/data/'



def Plot_Power_Spectrum_Grid_diff( output_dir, ps_data=None, scales='large', line_colors=None, sim_data_sets=None, black_background=False, high_z_only=False, plot_ps_normalized=False, ps_data_dir= root_dir + 'lya_statistics/data/', show_middle=False, 
                              ps_samples=None, data_labels=None, linewidth=1, line_color=None, line_alpha=1, c_boera=None, fig_name=None, plot_interval=False, plot_boeraC=False, HL_key='Highest_Likelihood' ):
  
  if system == 'Lux' or system == 'Summit': matplotlib.use('Agg')
  import matplotlib.pyplot as plt


  fig_height = 7
  fig_width = 16
  fig_dpi = 300
  
  if high_z_only: fig_height = 8

  label_size = 16
  figure_text_size = 18
  legend_font_size = 12
  tick_label_size_major = 15
  tick_label_size_minor = 13
  tick_size_major = 5
  tick_size_minor = 3
  tick_width_major = 1.5
  tick_width_minor = 1
  border_width = 1
  
  if not line_colors: line_colors = [ 'C0', 'C1', 'C2', 'C3', 'C4' ]

  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=11)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=11)
  if system == 'Tornado':  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=11)

  verbose = False
  
  dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
  data_boss = load_data_boss( dir_boss )
  data_z_boss = data_boss['z_vals']

  data_filename = ps_data_dir + 'data_power_spectrum_walther_2019/data_table.txt'
  data_walther = load_power_spectrum_table( data_filename )
  data_z_w = data_walther['z_vals']

  dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
  data_boera = load_data_boera( dir_data_boera, corrected=False, print_out=verbose )
  data_boera_c = load_data_boera( dir_data_boera, corrected=True, print_out=verbose )
  data_z_b = data_boera['z_vals']
  data_z_bc = data_boera_c['z_vals']

  data_dir_viel = ps_data_dir + 'data_power_spectrum_viel_2013/'
  data_viel = load_tabulated_data_viel( data_dir_viel)
  data_z_v = data_viel['z_vals']
  
  dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
  data_irsic = load_data_irsic( dir_irsic )
  data_z_irsic = data_irsic['z_vals']


  dir_gaikwad = ps_data_dir + 'data_gaikwad_2021/'
  data_filename = dir_gaikwad + 'Flux_Power_Spectrum_Observations.txt'
  data_gaikwad = load_data_gaikwad( data_filename )
  data_z_gaikwad = data_gaikwad['z_vals']
  
  
  file_name = ps_data_dir + 'simulated_power_spectrum_HM12_corrected.pkl'
  data_HM12 = Load_Pickle_Directory( file_name )
  print( data_HM12.keys() )
  data_boss = data_HM12['Boss']
  data_boera = data_HM12['Boera']
  data_irsic = data_HM12['Irsic']
  
  z_vals_small_scale  = [ 4.2, 4.6, 5.0, 5.4 ]
  z_vals_large_scale  = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4 ]
  z_vals_middle_scale = [   3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4  ]
  z_vals_small_scale_walther  = [ 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4,  ]
  z_vals_small_highz  = [ 4.2, 4.6, 5.0,  ]
  z_vals_small_highz_extended  = [ 4.2, 4.6, 5.0, 5.4  ]
  z_high = [ 5.0, 5.4 ]
  z_large_middle = [   3.0, 3.2, 3.4, 3.6, 3.8, 4.0,   ]
  z_vals_large_reduced  = [ 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0,  ]
  z_vals_small_reduced = [ 4.2, 4.6, 5.0 ]
  z_vals_all = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0,    ]
  z_vals_all_z2 = [ 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0,    ]
  z_vals_5 = [ 5.0 ]
  
  
  if scales == 'large': z_vals = z_vals_large_scale
  elif scales == 'small': z_vals = z_vals_small_scale
  elif scales == 'middle': z_vals = z_vals_middle_scale
  elif scales == 'small_walther': z_vals = z_vals_small_scale_walther
  elif scales == 'small_highz': z_vals = z_vals_small_highz
  elif scales == 'small_highz_extended': z_vals = z_vals_small_highz_extended
  elif scales == 'all': z_vals = z_vals_all
  elif scales == 'all_and_z2': z_vals = z_vals_all_z2
  elif scales == 'large_middle': z_vals = z_large_middle
  elif scales == 'large_reduced': z_vals = z_vals_large_reduced
  elif scales == 'small_reduced': z_vals = z_vals_small_reduced
  elif scales == 'large_small': z_vals = z_vals_small_reduced
  elif scales == 'small_z5': z_vals = z_vals_5
  else: 
    print( "ERROR: Scales = large,  small of middle ")
    return
    
  if high_z_only: z_vals = z_high
    
  nrows = 3
  ncols = 4
  
  
  if scales == 'small':  nrows, ncols = 1, 4
  if scales == 'small_walther': nrows = 2
  if high_z_only:    nrows, ncols = 1, 2
  if scales == 'large_middle': ncols, nrows = 3, 2

  
  if scales == 'all':  nrows, ncols = 3, 5
  if scales == 'middle':
    nrows = 2
    flags = np.zeros( (nrows, ncols ))
  
  if scales == 'small_highz':   nrows, ncols = 1, 3
  if scales == 'small_highz_extended':   nrows, ncols = 1, 4
  
  if scales == 'large_reduced': nrows, ncols = 2, 4
  if scales == 'small_reduced': nrows, ncols = 1, 3
  if scales == 'large_small': nrows, ncols = 1, 3
  
  
  plot_gaikwad = False
  plot_boss, plot_walther, plot_boera, plot_viel, plot_irsic = False, False, False, False, False
  
  if scales == 'large': plot_boss = True
  if scales == 'all': plot_boss, plot_boera, plot_irsic, plot_walther = True, True, True, True
  if scales == 'all_and_z2': plot_boss, plot_boera, plot_irsic, plot_walther = True, True, True, True
  if scales == 'middle': plot_boss, plot_irsic = True, True,
  if scales == 'small_highz': plot_boss, plot_boera = False, True,
  if scales == 'small_highz_extended': plot_viel, plot_boera = True, True
  if scales == 'small': plot_boera, plot_viel = True, True,
  if scales == 'large_middle': plot_boss, plot_irsic = True, True
  if scales == 'large_reduced': plot_boss = True
  if scales == 'large_small': plot_boss, plot_irsic, plot_boera = True, True, True
  if scales == 'small_reduced': 
    plot_boera = True
    fig_height *= 1.4
  if show_middle: plot_irsic = True
  if scales == 'small_z5': plot_boera = True
  if plot_boeraC and plot_boera:
    print( 'WRNING: Plotting Corrected Boera P(k)')
    # plot_boera = False
  
  plot_walther  = False
  
  if scales == 'small_z5': 
    ncols, nrows = 1, 1
    fig_width = 8 /1.5
    fig_height = 8 / 1.5
    label_size = 15
    figure_text_size = 15
    legend_font_size = 12
    tick_label_size_major = 13
    
  # plot_gaikwad = True
  # plot_walther  = True
  
  if scales == 'all':  
    nrows, ncols = 3, 5
    fig_height = 4

  
  if scales == 'all_and_z2':  
    nrows, ncols = 3, 5
    fig_height = 5
  
  hspace = 0.02
  # if show_middle: hspace = 0.1
  
  f = 4
  main_length = 6 * f
  sub_length = 2 * f
  h_length = main_length + sub_length + 1

  fig = plt.figure(0)
  fig.set_size_inches(fig_width, fig_height*nrows )
  fig.clf()

  gs = plt.GridSpec(h_length*nrows, ncols)
  gs.update(hspace=0.0, wspace=0.02, )


  

  c_pchw18 = pylab.cm.viridis(.7)
  c_hm12 = pylab.cm.cool(.3)
  # 
  # c_boss = pylab.cm.viridis(.3)
  # c_walther = pylab.cm.viridis(.3)
  # c_viel = 'C1'
  # c_boera = pylab.cm.Purples(.7)
  # c_irsic = pylab.cm.Purples(.7)
  
  c_boss = dark_blue
  if c_boera is None: c_boera = dark_green
  # if c_boera is None: c_boera = ocean_blue
  # c_boera = 'C2'
  
  c_boera_c = 'C4'
  
  
  c_viel = 'C1'
  c_viel = 'C9'
  c_gaikwad = 'C1'
  
  c_irsic = purple
  c_walther = 'C3'
  
  c_walther = purple
  c_irsic = 'C3'
  
  
  text_color  = 'black'
  color_line = c_pchw18
  
  if scales == 'middle':
    c_walther = 'C3'
  
  text_color = 'black'
    
  if black_background:
    text_color = 'white'
    c_boss = blues[5]
    c_irsic = light_orange
    # c_boera = yellows[0]
    blue = blues[4]
    color_line = blue

  c_boss = c_boera = c_irsic = 'C4'
  

  for index, current_z in enumerate( z_vals ):



    indx_j = index % ncols
    indx_i = index//ncols


    ax  = plt.subplot(gs[indx_i*h_length:indx_i*h_length+main_length, indx_j])
    ax1 = plt.subplot(gs[indx_i*h_length+main_length:indx_i*h_length+main_length+sub_length, indx_j])
  
    
    if scales == 'middle': flags[indx_i,  indx_j] = 1
    
    if ps_data:
      for sim_id in ps_data:
        data_sim = ps_data[sim_id]
        if 'label' in data_sim: label = data_sim['label']
        else: label = ''
        sim_z_vals = data_sim['z_vals']
        diff = np.abs( sim_z_vals - current_z )
        diff_min = diff.min()
        if diff_min > 5e-2: continue
        index = np.where( diff == diff_min )[0][0]
        data = data_sim[index]
        k = data['k_vals']
        ps = data['ps_mean']
        # delta = ps * k / np.pi 
        delta = ps
        factor = 1.0
        # if current_z == 4.6: factor = 1.1
        # if current_z == 5.0: factor = 1.1
        delta *= factor
        # color_line = line_colors[sim_id]
        if line_color is not None: line_color = line_color
        else: line_color = 'C0' 
        if 'line_color' in data_sim: line_color = data_sim['line_color']
        ax.plot( k, delta,  label=label, linewidth=linewidth,  zorder=1, color=line_color, alpha=line_alpha )
        # ax.plot( k, delta,  label=label, linewidth=linewidth,  zorder=1,  alpha=line_alpha )
        if plot_interval:
          high = data['higher'] * factor
          low = data['lower'] * factor
          ax.fill_between( k, high, low, color=line_color, alpha=0.4)
          
        
    if ps_samples is not None:
      for sim_id in ps_samples:
        factor = 1.0
        if current_z == 5.0:   factor = 1.05        
        if current_z == 4.6:   factor = 1.05        
        data_sim = ps_samples[sim_id]
        if data_labels is not None: label = data_labels[sim_id]
        else: label = ''
        if 'label' in data_sim: label = data_sim['label']
        
        sim_z_vals = data_sim['z_vals']
        diff = np.abs( sim_z_vals - current_z )
        diff_min = diff.min()
        index = np.where( diff == diff_min )[0][0]
        data = data_sim[index]
        k = data['k_vals']
        delta = data[HL_key] * factor
        if 'line_color' in data_sim: line_color = data_sim['line_color']
        else: line_color = 'C0' 
        ls = '-'
        if 'ls' in data_sim: ls = data_sim['ls']
        lw = 1.5
        if 'lw' in data_sim: ls = data_sim['lw']
        ax.plot( k, delta, linewidth=lw, label=label, zorder=1, color=line_color, ls=ls  )        
        k_reference, delta_reference = k, delta
        ax1.axhline( y=0, linewidth=lw, label=label, zorder=1, color=line_color, ls=ls )
        # if sim_id == 0:
        if 'higher' in data:
          high = data['higher'] * factor
          low  = data['lower'] * factor
          # high *= 1.05
          # low *= 0.95
          high *= 1.03
          low *= 0.97
          ax.fill_between( k, high, low, color=line_color, alpha=0.4 )
          high = ( high - delta_reference ) / delta_reference
          low  = ( low  - delta_reference ) / delta_reference
          ax1.fill_between( k, high, low, color=line_color, alpha=0.4 )
          
    if sim_data_sets:
      for sim_data in sim_data_sets:
        # sim_z_vals = sim_data['z']
        # diff = np.abs( sim_z_vals - current_z )
        # diff_min = diff.min()
        # index = np.where( diff == diff_min )[0][0]
        # # print( index )
        # if diff_min < 0.08:
        #   k = sim_data['ps_kvals'][index]
        #   ps = sim_data['ps_mean'][index]
        #   delta = ps * k / np.pi 
        #   ax.plot( k, delta, linewidth=3, label=sim_data['plot_label'], zorder=1  )
        #   # ax.plot( k, delta, c=color_line, linewidth=3, label=sim_data['plot_label']  )
        # 
        if plot_ps_normalized:
          ps_data = sim_data['power_spectrum_normalized']
          name = ps_data['normalization_key'] 
        else: ps_data = sim_data['power_spectrum']
        sim_z_vals = ps_data['z']
        diff = np.abs( sim_z_vals - current_z )
        diff_min = diff.min()
        index = np.where( diff == diff_min )[0][0]
        # print( index )
        if diff_min < 0.08:
          k = ps_data['k_vals'][index]
          ps = ps_data['ps_mean'][index]
          delta = ps * k / np.pi 
          ax.plot( k, delta, linewidth=3, label=sim_data['plot_label'], zorder=1  )
          # ax.plot( k, delta, c=color_line, linewidth=3, label=sim_data['plot_label']  )
          

    text_pos_x = 0.85
    if scales == 'all': text_pos_x = 0.82
    if scales == 'all_and_z2': text_pos_x = 0.82
    if scales == 'large_reduced': text_pos_x = 0.15
    ax.text(text_pos_x, 0.93, r'$z=${0:.1f}'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

    
    if plot_boss:
      # Add Boss data
      z_diff = np.abs( data_z_boss - current_z )
      diff_min = z_diff.min()
      label_boss = 'eBOSS (2019)'
      if diff_min < 1e-1:
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_boss[data_index]
        data_k = data_boss[data_index]['k_vals']
        data_delta_power = data_boss[data_index]['delta_power']
        data_delta_power_error = data_boss[data_index]['delta_power_error']
        d_boss = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boss, label='', zorder=2)

        indices = ( data_k >= k_reference.min() ) * ( data_k <= k_reference.max())
        data_k = data_k[indices]
        data_delta_power = data_delta_power[indices]
        data_delta_power_error = data_delta_power_error[indices]
        delta_interp = interpolate_1d_linear( data_k, k_reference, delta_reference, log_y=True )
        data_delta_power = ( data_delta_power - delta_interp ) / delta_interp
        data_delta_power_error =  data_delta_power_error / delta_interp
        d_boss = ax1.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boss, label='', zorder=2)
        
                
      if indx_i == 0 and indx_j == 0:
        label_boss = 'HM12'
        ax.errorbar( [1e2], [1e2], yerr=1, fmt='o', c=c_boss, label=label_boss, zorder=2)
        

    # Add Irsic data
    if plot_irsic:
      z_diff = np.abs( data_z_irsic - current_z )
      diff_min = z_diff.min()
      factor = 1.0
      label_irsic = 'Irsic et al. (2017)'
      label_irsic = ''
      if diff_min < 1e-1:
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_irsic[data_index]

        data_k = data_irsic[data_index]['k_vals']
        data_delta_power = data_irsic[data_index]['delta_power']
        data_delta_power_error = data_irsic[data_index]['delta_power_error']
        if current_z == 3.2: factor = 0.96
        if current_z == 4.2: factor = 1.04
        data_delta_power *= factor
        d_irsic = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_irsic, label='', zorder=2)

        indices = ( data_k >= k_reference.min() ) * ( data_k <= k_reference.max())
        data_k = data_k[indices]
        data_delta_power = data_delta_power[indices]
        data_delta_power_error = data_delta_power_error[indices]
        delta_interp = interpolate_1d_linear( data_k, k_reference, delta_reference, log_y=True )
        data_delta_power = ( data_delta_power - delta_interp ) / delta_interp 
        data_delta_power_error =  data_delta_power_error / delta_interp
        d_irsic = ax1.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_irsic, label='', zorder=2)
        
        
      if indx_i == 1 and indx_j == 0:
        ax.errorbar( [1e2], [1e2], yerr=1, fmt='o', c=c_irsic, label=label_irsic, zorder=2)
        
    if plot_boera:
      label_boera ='Boera et al. (2019)'
      label_boera = ''
      # Add Boera data
      z_diff = np.abs( data_z_b - current_z )
      diff_min = z_diff.min()
      factor = 1.0
      if diff_min < 1e-1:
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_b[data_index]
        data_k = data_boera[data_index]['k_vals']
        data_delta_power = data_boera[data_index]['delta_power']
        data_delta_power_error = data_boera[data_index]['delta_power_error']
        if current_z == 4.2: factor = 0.97
        data_delta_power *= factor
        d_boera = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boera, label=label_boera, zorder=2 )

        indices = ( data_k >= k_reference.min() ) * ( data_k <= k_reference.max())
        data_k = data_k[indices]
        data_delta_power = data_delta_power[indices]
        data_delta_power_error = data_delta_power_error[indices]
        delta_interp = interpolate_1d_linear( data_k, k_reference, delta_reference, log_y=True )
        data_delta_power = ( data_delta_power - delta_interp ) / delta_interp
        data_delta_power_error =  data_delta_power_error / delta_interp
        d_boera = ax1.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boera, label=label_boera, zorder=2 )
        # 
      if indx_i == 2 and indx_j == 0:
        ax.errorbar( [1e2], [1e2], yerr=1, fmt='o', c=c_boera, label=label_boera, zorder=2)
        
    if plot_boeraC:
      # Add Boera data
      z_diff = np.abs( data_z_bc - current_z )
      diff_min = z_diff.min()
      factor = 1.0
      if diff_min < 1e-1:
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_bc[data_index]
        data_k = data_boera_c[data_index]['k_vals']
        data_delta_power = data_boera_c[data_index]['delta_power']
        data_delta_power_error = data_boera_c[data_index]['delta_power_error']
        label_boera ='Boera et al. (2019) Corrected'
        # if current_z == 4.2: factor = 0.97
        data_delta_power *= factor
        d_boera = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boera_c, label=label_boera, zorder=2 )

    
    if plot_walther:
      label_walther ='Walther et al. (2018)' 
      # Add Walther data
      z_diff = np.abs( data_z_w - current_z )
      diff_min = z_diff.min()
      k_max = 0.1
      if diff_min < 1e-1:
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_w[data_index]
        data_k = data_walther[data_index]['k_vals']
        indices = data_k <= k_max
        data_k = data_k[indices] 
        data_delta_power = data_walther[data_index]['delta_power'][indices]
        data_delta_power_error = data_walther[data_index]['delta_power_error'][indices]
        mfc = 'w'
        if black_background: mfc = 'k'
        d_walther = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_walther,   label='', zorder=2, mfc=mfc)

        indices = ( data_k >= k_reference.min() ) * ( data_k <= k_reference.max())
        data_k = data_k[indices]
        data_delta_power = data_delta_power[indices]
        data_delta_power_error = data_delta_power_error[indices]
        delta_interp = interpolate_1d_linear( data_k, k_reference, delta_reference, log_y=True )
        data_delta_power = ( data_delta_power - delta_interp ) / delta_interp
        data_delta_power_error =  data_delta_power_error / delta_interp
        d_walther = ax1.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_walther,   label='', zorder=2, mfc=mfc)
        
      if indx_i == 0 and indx_j == 0:
        ax.errorbar( [1e2], [1e2], yerr=1, fmt='o', c=c_walther, label=label_walther, zorder=2, mfc=mfc)
    
    if plot_viel:
      # Add Viel data
      z_diff = np.abs( data_z_v - current_z )
      diff_min = z_diff.min()
      # if diff_min < 1e-1 and current_z == 5.4:
      if diff_min < 1e-1 :
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_v[data_index]
        data_k = data_viel[data_index]['k_vals']
        data_delta_power = data_viel[data_index]['delta_power']
        data_delta_power_error = data_viel[data_index]['delta_power_error']
        label_viel = 'Viel et al. (2013)'
        d_viel = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_viel, label=label_viel, zorder=2 )

    if plot_gaikwad:
      # Add Gaikwad data
      z_diff = np.abs( data_z_gaikwad - current_z )
      diff_min = z_diff.min()
      if diff_min < 1e-1 :
        data_index = np.where( z_diff == diff_min )[0][0]
        data_z_local = data_z_gaikwad[data_index]
        data_k = data_gaikwad[data_index]['k_vals']
        data_delta_power = data_gaikwad[data_index]['delta_power'] 
        data_delta_power_error = data_gaikwad[data_index]['delta_power_error']
        label_gaikwad = 'Gaikwad et al. (2021)'
        d_gaikwad = ax.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_gaikwad, label=label_gaikwad, zorder=2 )

    legend_loc = 3
    if indx_i == nrows-1 and nrows!=2: legend_loc = 2
    
    if scales == 'large': legend_loc = 2
    if scales == 'middle': legend_loc = 2
    if scales == 'small_highz': legend_loc = 3
    if scales == 'large_middle': legend_loc = 2
    if scales == 'large_reduced': legend_loc = 4
    
    label_bars =  r'1$\sigma$ skewers $P\,(\Delta_F^2)$'

    add_legend = False
    if indx_j == 0: add_legend = True
    
    # if scales == 'middle' and indx_i == nrows-1 and indx_j == ncols-1: add_legend = True
    
    if scales == 'large_small': legend_loc = 3
    if scales == 'small_z5': legend_loc = 3
    
    if scales == 'all':
      if indx_i == 0: legend_loc = 2
      if indx_i == 1: legend_loc = 2
      if indx_i == 2: legend_loc = 3
    
    if scales == 'all_and_z2':
      if indx_i == 0: legend_loc = 2
      if indx_i == 1: legend_loc = 2
      if indx_i == 2: legend_loc = 3
      
    if add_legend:
      # leg = ax.legend( loc=legend_loc, frameon=False, fontsize=12)
      leg = ax.legend(  loc=legend_loc, frameon=False, fontsize=legend_font_size    )
      
      for text in leg.get_texts():
          plt.setp(text, color = text_color)
          



    x_min, x_max = 4e-3, 2.5e-1
    if indx_i == 0: y_min, y_max = 1e-3, 9e-2
    if indx_i == 1: y_min, y_max = 5e-3, 2e-1
    if indx_i == 2: y_min, y_max = 5e-2, 3

    if scales == 'large':
      x_min, x_max = 2e-3, 2.3e-2
      if indx_i == 0: y_min, y_max = 1e-2, 1.2e-1
      if indx_i == 1: y_min, y_max = 2e-2, 2.5e-1
      if indx_i == 2: y_min, y_max = 5e-2, 7e-1

    if scales == 'middle':
      x_min, x_max = 2e-3, 7e-2
      if indx_i == 0: y_min, y_max = 1.8e-2, 2.5e-1
      if indx_i == 1: y_min, y_max = 5e-2, 7e-1
    
    if scales == 'all':
      x_min, x_max = 4e-3, 2.5e-1
      if indx_i == 0: y_min, y_max = 1e-3, 9e-2
      if indx_i == 1: y_min, y_max = 5e-3, 2e-1
      if indx_i == 2: y_min, y_max = 5e-2, 3
  

    if scales == 'small_highz':
      x_min, x_max = 4.5e-3, 2.4e-1
      if indx_i == 0: y_min, y_max = 5e-3, 1e0
      
    if scales == 'small_highz_extended':
      x_min, x_max = 3e-3, 1.7e-1
      if indx_i == 0: y_min, y_max = 3e-2, 3e0
      
    if scales == 'large_middle':
      x_min, x_max =  2e-3, 7e-2
      if indx_i == 0: y_min, y_max = 2e-2, 1.5e-1
      if indx_i == 1: y_min, y_max = 4e-2, 3.5e-1
    
    if scales == 'large_reduced':
      x_min, x_max = 2e-3, 2.5e-2
      if indx_i == 0: y_min, y_max = 1.2e-2, 1.3e-1
      if indx_i == 1: y_min, y_max = 2.5e-2, 4e-1

      
    if scales == 'large_reduced':
      x_min, x_max = 2e-3, 2.5e-2
      if indx_i == 0: y_min, y_max = 1.2e-2, 1.3e-1
      if indx_i == 1: y_min, y_max = 2.5e-2, 4e-1
      
    if scales == 'small_reduced':
      # x_min, x_max = 4e-3, 2e-1
      x_min, x_max = 2e-3, 1.5e-1
      if indx_i == 0: y_min, y_max = 2.5e-2, 8e-1

    if scales == 'small':
      x_min, x_max = 4e-3, 3e-1
      if indx_i == 0: y_min, y_max = 8e-3, 2e-0
      
    if show_middle:
      if indx_i == 0: x_min, x_max = 2e-3, 2.3e-2      
      # if indx_i == 0: x_min, x_max = 2e-3, 2.3e-2
      if indx_i == 0: x_min, x_max = 2e-3, 7e-2
      if indx_i == 1: x_min, x_max = 2e-3, 7e-2
      if indx_i == 2: 
        x_min, x_max = 2e-3, 7e-2 
        # if indx_j == 3: x_min, x_max = 2e-3, 2.3e-2 
        
    if scales == 'large_small':
      x_min, x_max = 2e-3, 1.5e-1
      y_min, y_max = 1e-2, 9e-1
  
    if scales == 'all':
      # x_min, x_max = 2e-3, 1.5e-1
      # if indx_i == 0: y_min, y_max = 8e-3, 1.1e-1
      # if indx_i == 1: y_min, y_max = 2.5e-2, 3.5e-1
      # if indx_i == 2: y_min, y_max = 2.5e-2, 2e-0
      x_min, x_max = 2e-3, 2.2e-1
      if indx_i == 0: y_min, y_max = 8e-3, 1.1e-1
      if indx_i == 1: y_min, y_max = 2.e-2, 3.5e-1
      if indx_i == 2: y_min, y_max = 8.e-3, 1e-0
      
    if scales == 'all_and_z2':
      # x_min, x_max = 2e-3, 1.5e-1
      # if indx_i == 0: y_min, y_max = 8e-3, 1.1e-1
      # if indx_i == 1: y_min, y_max = 2.5e-2, 3.5e-1
      # if indx_i == 2: y_min, y_max = 2.5e-2, 2e-0
      x_min, x_max = 2e-3, 2.2e-1
      if indx_i == 0: y_min, y_max = 6e-3, 9e-2
      if indx_i == 1: y_min, y_max = 6.e-3, 2.5e-1
      if indx_i == 2: y_min, y_max = 7.e-3, 8e-1
      
    if scales == 'small_z5':
      x_min, x_max = 2e-3, 2.2e-1
      y_min, y_max = 1e-2, 8e-1

      
    if high_z_only: y_min, y_max = 5e-2, 3
    
  


    ax.set_xlim( x_min, x_max )
    ax.set_ylim( y_min, y_max )
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_xlim( x_min, x_max )
    ax1.set_ylim( -0.5, 0.5 )
    if indx_i == nrows-1: ax1.set_ylim( -0.9, 0.9 )
    

    [sp.set_linewidth(border_width) for sp in ax.spines.values()]


    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax1.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax1.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


    # if indx_i != nrows-1 and not show_middle:ax.set_xticklabels([])
    # if indx_i != nrows-1 :ax.set_xticklabels([])
    if nrows > 1 and indx_i != nrows - 1 :
      ax.set_xticklabels([])
      ax1.set_xticklabels([])
  
    # if indx_i == 1 and indx_j != 4 :
    #   ax.set_xticklabels([])
    #   ax.set_xticklabels([])
  
    if indx_j > 0:
      ax.set_yticklabels([])
      ax.tick_params(axis='y', which='minor', labelsize=0 )
      ax1.set_yticklabels([])
      ax1.tick_params(axis='y', which='minor', labelsize=0 )



    if indx_j == 0: 
      ax.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size, color= text_color )
      ax1.set_ylabel( r'$\Delta P\,(k) / P\,(k) $', fontsize=label_size-2, color= text_color )
    
    # if indx_i == nrows-1: ax.set_xlabel( r'$ k   \,\,\,  [\mathrm{s}\,\mathrm{km}^{-1}] $',  fontsize=label_size, color= text_color )
    if indx_i == nrows-1 : ax1.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )
    if scales == 'all' and indx_i == nrows-2 and indx_j==4: ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )

    if black_background: 
      fig.patch.set_facecolor('black') 
      ax.set_facecolor('k')
      [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]

  if scales == 'all' :
    ax = ax_l[2][4]
    print( 'Turning axis off')
    ax.set_axis_off()
    
      
  if scales == 'middle':
    for i in range( nrows ):
      for j in range( ncols ):
        if not flags[i,j]:
          ax = ax_l[i][j].axis('off')
          
  

          
        
  
  fileName = output_dir + f'flux_ps_grid_{scales}'
  if plot_ps_normalized: fileName += f'_{name}'
  if high_z_only: fileName += '_highZ'
  fileName += '_diff'
  fileName += '.png'
  # fileName += '.pdf'
  if fig_name is not None: fileName = output_dir + fig_name
  fig.savefig( fileName,  pad_inches=0.1, bbox_inches='tight', dpi=fig_dpi, facecolor=fig.get_facecolor())
  print('Saved Image: ', fileName)



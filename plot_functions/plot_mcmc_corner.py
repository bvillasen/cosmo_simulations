import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
root_dir = os.path.dirname(os.getcwd())  + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from figure_functions import *
from stats_functions import get_HPI_2D, get_highest_probability_interval



def Plot_Corner( samples, data_label, labels, output_dir, n_bins_1D=20, n_bins_2D=30, 
    ticks=None, lower_mask_factor=50, multiple=False, system='Shamrock', show_label=True, 
    HL_vals=None, show_best_fit=False, limits=None, param_values=None, black_background=False,
    bins=None, legend_loc=0, figure_name='corner.png', show_param_values=False ):
  
  

  
  if not multiple:
    data_labels = [data_label]
    samples_multiple = {}
    samples_multiple[0] = samples
  else: 
    data_labels = data_label
    samples_multiple = samples
    
  samples = samples_multiple[0]  
  param_ids = samples.keys()
  n_param = len( param_ids )

      
  color = 'C0'
  data_color = 'C9'
  font_size = 22
  legend_font_size = 16
  label_size = 30
  alpha = 0.6
  fig_size = 5
  space = 0.05
  
  n_tricks = 6
  
  tick_label_size = 16
  tick_length = 7
  tick_width = 2
  border_width = 2.0
  hist_1D_line_width = 3.09
  hist_1D_line_color = 'C0'
  hist_2D_colormap = palettable.cmocean.sequential.Ice_20_r.mpl_colormap
  
  color_map_0 = palettable.cmocean.sequential.Ice_20_r
  color_map_1 = palettable.cmocean.sequential.Amp_20
  color_map_2 = palettable.cmocean.sequential.Tempo_20
  color_map_3 = palettable.cmocean.sequential.Dense_20
  color_map_4 = palettable.cmocean.sequential.Algae_20
  color_map_5 = palettable.scientific.sequential.Devon_20_r
  color_map_6 = palettable.scientific.sequential.Davos_20_r
  color_map_7 = palettable.scientific.sequential.LaPaz_20_r
  color_map_7 = palettable.scientific.sequential.Oslo_20_r
  # color_map_list = [ color_map_0, color_map_2, color_map_1, color_map_4 ]
  color_map_list = [ color_map_7 ]
  
  text_color = 'black'
  
  hl_line_color = 'black'
  hl_color = 'gray' 
  hl_line_width = 2.5 
  hl_alpha = 1.0
  
  marker_color = 'white'
  
  # black_background = False
  if black_background:
    color_map_0 = palettable.cmocean.sequential.Ice_20
    # color_map_0 = palettable.matplotlib.Inferno_20
    color_map_list = [ color_map_0, color_map_1, color_map_3, color_map_3, color_map_4 ]
    text_color = 'white'
    tick_label_size = 18
    label_size = 32
    marker_color = 'black'

  sharex = 'col'
  if ticks is not None: sharex = 'none'
  fig, ax_l = plt.subplots(nrows=n_param, ncols=n_param, figsize=(fig_size*n_param,fig_size*n_param),  sharex=sharex )
  fig.subplots_adjust( wspace=space, hspace=space )

  distribution_data = {}
  for j in range( n_param ):
    for i in range( n_param ):
      
      add_data_label = False
      if i== 0 and j == 0: add_data_label = True

      ax = ax_l[j][i]
      plot_y_lables, plot_x_lables = False, False
      plot_y_ticks  = True
      if i == 0: plot_y_lables = True
      if j == n_param-1: plot_x_lables = True 
      if i == j: 
        plot_y_lables = False
        plot_y_ticks = False

      if i > j:
        ax.axis("off")
        continue

      if plot_x_lables: ax.tick_params(axis='x', which='major', direction='in', labelsize=tick_label_size, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
      else:             ax.tick_params(axis='x', which='major', direction='in', labelsize=0, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
      if plot_y_lables: ax.tick_params(axis='y', which='major', direction='in', labelsize=tick_label_size, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
      else:             ax.tick_params(axis='y', which='major', direction='in', labelsize=0, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
      if not plot_y_ticks: ax.tick_params(axis='y', which='major', length=0 )

      if plot_y_lables:
        if j == 0: y_label = ''
        else: y_label = labels[samples[j]['name']]  
        ax.set_ylabel( y_label, fontsize=label_size, color=text_color )

      if plot_x_lables:
        x_label = labels[samples[i]['name']]  
        ax.set_xlabel( x_label, fontsize=label_size, color=text_color )
        
      
      if i == j: plot_type = '1D'
      if i < j:  plot_type = '2D'
      
      
      for data_id in samples_multiple:
        samples = samples_multiple[data_id]
        
        colormap = color_map_list[data_id]
        hist_2D_colormap = colormap.mpl_colormap
        contour_colormap = colormap.mpl_colors
        n_colors = len( contour_colormap )
        line_color = contour_colormap[n_colors//2]
        if black_background: line_color = palettable.colorbrewer.sequential.Blues_9_r.mpl_colors[4]
        contour_colors = [contour_colormap[n_colors//2], contour_colormap[-1]]
        
        if plot_type == '1D':
          name  = samples[j]['name']
          trace = samples[j]['trace']
          bins_1D = n_bins_1D 
          if bins is not None and bins[j] is not None: 
            bin_min, bin_max, n_bin = bins[j]['min'], bins[j]['max'], bins[j]['n'] 
            bins_1D = np.linspace( bin_min, bin_max, n_bin )
            print( f"Bins 1D: {bins_1D}" )
          hist, bin_edges = np.histogram( trace, bins=bins_1D ) 
          # hist = hist / hist.sum()
          bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
          bin_width = bin_centers[0] - bin_centers[1]  
          bin_centers_interp = np.linspace( bin_centers[0], bin_centers[-1], 100000 )
          f_interp  = interp.interp1d( bin_centers, hist,  kind='cubic' )
          data_label = data_labels[data_id]
          if add_data_label: label = f'{data_label}' 
          else: label = ''
          ax.plot( bin_centers_interp, f_interp(bin_centers_interp),   color=line_color, linewidth=hist_1D_line_width, label=label, zorder=3  )
          # ax.plot( bin_centers, hist,   color=line_color, linewidth=hist_1D_line_width  ), 
          # ax.step( bin_centers, hist, where='mid',  color=line_color, linewidth=hist_1D_line_width  )
          distribution = hist/hist.sum()
          if HL_vals is not None:
            # print(HL_vals)
            hl_val = HL_vals[j]
            # print( f_interp(hl_val), f_interp(bin_centers_interp).max())
            # ax.axvline( x=hl_val, ymin=0, ymax=f_interp(hl_val)[0], ls='--', lw=hl_line_width, color=hl_color, alpha=hl_alpha )
            ax.plot( [hl_val, hl_val], [-1*f_interp(hl_val), f_interp(hl_val)], ls='--', lw=hl_line_width, color=hl_line_color, alpha=hl_alpha, zorder=2 )
            fill_sum = 0.68
            v_l, v_r, v_max,  sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=100000, print_eval=False)
            print( f'Eval f(l): {f_interp(v_l)}  f(r): {f_interp(v_r)}  sum: {sum}')
            vals_simgna = np.linspace( v_l, v_r, 1000 )
            sigma_l = hl_val - v_l
            sigma_r = v_r - hl_val
            ax.fill_between( vals_simgna, f_interp(vals_simgna), color=hl_color, alpha=0.5, zorder=1)
            fill_sum = 0.95
            v_l, v_r, v_max,  sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=100000, print_eval=False)
            print( f'Eval f(l): {f_interp(v_l)}  f(r): {f_interp(v_r)}  sum: {sum}')
            vals_simgna = np.linspace( v_l, v_r, 1000 )
            two_sigma_l = hl_val - v_l
            two_sigma_r = v_r - hl_val
            ax.fill_between( vals_simgna, f_interp(vals_simgna), color=hl_color, alpha=0.3, zorder=1)
            distribution_data[j] = {'HL':hl_val, 'sigma_l':sigma_l, 'sigma_r':sigma_r, 'two_sigma_l':two_sigma_l, 'two_sigma_r':two_sigma_r, }
            
          def identity( x ):
            return x
          secax = ax.secondary_xaxis('top', functions=(identity, identity))    
          secax.tick_params(axis='x', which='major', direction='in', labelsize=tick_label_size, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
          x_label = labels[samples[j]['name']]  
          secax.set_xlabel( x_label, fontsize=label_size, color=text_color, labelpad=15 )
          if ticks is not None: secax.set_ticks(ticks[j])

                      
          max = f_interp(bin_centers_interp).max()
          # ax.set_ylim( -max/20, max*1.1 )
        
        if plot_type == '2D':
          trace_y = samples[j]['trace']
          trace_x = samples[i]['trace']
          hist, x_edges, y_edges = np.histogram2d( trace_x, trace_y, bins=[n_bins_2D, n_bins_2D] )
          hist = hist.astype( np.float ) 
          # hist = hist.T / hist.sum()
          hist = hist.T 
          extent = [ trace_x.min(), trace_x.max(), trace_y.min(), trace_y.max() ]
          hist_2D = hist
          level_95, indices_enclosed = get_HPI_2D( hist_2D, 0.95 )
          level_68, indices_enclosed = get_HPI_2D( hist_2D, 0.68 )            
          lower = hist_2D.max() / lower_mask_factor
          hist_2D_masked = np.ma.masked_where( hist_2D < lower, hist_2D )
          ax.imshow( hist_2D_masked[::-1], cmap=hist_2D_colormap, extent=extent, aspect='auto', interpolation='bilinear' )
          # ax.contour( hist, [hist_sigma, 2* hist_sigma], extent=extent, colors= contour_colors, linewidths=2 )
          ax.contour( hist, [level_95,  level_68], extent=extent, colors= contour_colors, linewidths=2 )
          if HL_vals is not None:
            hl_val_x = HL_vals[j]
            hl_val_y = HL_vals[i]
            # ax.axvline( x=hl_val_y, ls='--', lw=hl_line_width, color=hl_color, alpha=hl_alpha )
            # ax.axhline( y=hl_val_x, ls='--', lw=hl_line_width, color=hl_color, alpha=hl_alpha )
            ax.scatter( (hl_val_y), (hl_val_x) ,c=marker_color)
          
        
        if add_data_label and show_label:
          leg = ax.legend( loc=legend_loc, frameon=False, fontsize=legend_font_size)
          for text in leg.get_texts():
            plt.setp(text, color = text_color)
            
      [sp.set_linewidth(border_width) for sp in ax.spines.values()]
      
      if black_background: 
        fig.patch.set_facecolor('black') 
        ax.set_facecolor('k')
        [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
          
      
      # ax.xaxis.set_major_locator(plt.MaxNLocator(n_tricks))
      # ax.yaxis.set_major_locator(plt.MaxNLocator(n_tricks))
  
  # fig.align_ylabels(ax_l[:, 1])
  for j in range(n_param):
    labelx = -0.2
    # if j == 1: labelx = -0
    ax_l[j, 0].yaxis.set_label_coords(labelx, 0.5)
    
  if ticks is not None:  
    for j in range( n_param ):
      for i in range( n_param ):
        ax = ax_l[j][i]
        ax.set_xticks(ticks[i])
        ax.set_yticks(ticks[j])
        
  if limits is not None:  
    for j in range( n_param ):
      for i in range( n_param ):
        ax = ax_l[j][i]
        x_lims = limits[i]
        y_lims = limits[j] 
        ax.set_xlim( x_lims[0], x_lims[1] )
        if j > i: ax.set_ylim( y_lims[0], y_lims[1] )
        if j == i: ax.set_ylim(-1,None)

  
  if show_param_values:
    text_x = 0.6
    text_y = 0.855 
    delta_y = 0.05
    print( distribution_data )
    for param_id in samples:
      param_data = samples[param_id]
      name = param_data['name']
      label = labels[name]
      text = label + f' = {distribution_data[param_id]["HL"]:.2f}' #+ '^{+' + f'{distribution[param_id]["sigma_r"]}' +'}_{-' +  f'{distribution[param_id]["sigma_l"]}'  + '}'  
      plt.text( text_x, text_y, r'${0}$'.format(text), transform=fig.transFigure, fontsize=26, color=text_color )
      text_y -= delta_y
      
      
  if param_values is not None:
    offset_y_add = 0.02
    font_add = 4
    text_x = 0.46
    text_y = 0.855 + offset_y_add
    text = '95% Confidence Interval:'  
    plt.text( text_x, text_y, text, transform=fig.transFigure, fontsize=22+font_add, color=text_color )
    
    p_name = 'scale_H'
    p_vals = param_values[p_name]
    val = p_vals['value']
    delta_h = p_vals['delta_h']
    delta_l = p_vals['delta_l']  
    label = labels[p_name][1:-1]
    text_0 =  f'{label}' + ' \,\,= \mathregular{ ' + f'{val:.2f}' + '}^{+\mathregular{' + f'{delta_h:.2f}' + '}}_{-\mathregular{' +f'{delta_l:.2f}' + '}}'
    
    p_name = 'scale_He'
    p_vals = param_values[p_name]
    val = p_vals['value']
    delta_h = p_vals['delta_h']
    delta_l = p_vals['delta_l']  
    label = labels[p_name][1:-1]
    text_1 =  f'{label}' + ' = \mathregular{ ' + f'{val:.2f}' + '}^{+\mathregular{' + f'{delta_h:.2f}' + '}}_{-\mathregular{' +f'{delta_l:.2f}' + '}}'
    
    # text_1 = r'$\beta_{\mathrm{He}}=\mathregular{0.44}^{+\mathregular{0.06}}_{-\mathregular{0.07}}$'
    text_lines = [ r'${0}$'.format(text_0) , r'${0}$'.format(text_1) ]
    # text_x = 0.56
    text_y = 0.82 + offset_y_add
    offset_y = 0.05
    for text in text_lines:
      plt.text( text_x, text_y, text, transform=fig.transFigure, fontsize=25+font_add, color=text_color )
      text_y -= offset_y
    
    p_name = 'deltaZ_H'
    p_vals = param_values[p_name]
    val = p_vals['value']
    delta_h = p_vals['delta_h']
    delta_l = p_vals['delta_l']  
    label = labels[p_name][1:-1]
    text_0 =  f'{label}' + ' \,\,= \mathregular{ ' + f'{val:.2f}' + '}^{+\mathregular{' + f'{delta_h:.2f}' + '}}_{-\mathregular{' +f'{delta_l:.2f}' + '}}'
    
    p_name = 'deltaZ_He'
    p_vals = param_values[p_name]
    val = p_vals['value']
    delta_h = p_vals['delta_h']
    delta_l = p_vals['delta_l']  
    label = labels[p_name][1:-1]
    text_1 =  f'{label}' + ' = \mathregular{ ' + f'{val:.2f}' + '}^{+\mathregular{' + f'{delta_h:.2f}' + '}}_{-\mathregular{' +f'{delta_l:.2f}' + '}}'
    
    # text_lines = [ r'$\Delta z_{\mathrm{H}}\,\,=\mathregular{0.05}^{+\mathregular{0.03}}_{-\mathregular{0.03}}$', r'$\Delta z_{\mathrm{He}}=\mathregular{0.27}^{+\mathregular{0.06}}_{-\mathregular{0.06}}$', ]
    text_lines = [ r'${0}$'.format(text_0) , r'${0}$'.format(text_1) ]
    
    text_x = text_x + .2
    text_y = 0.82 + offset_y_add
    # offset_y = 0.04
    for text in text_lines:
      plt.text( text_x, text_y, text, transform=fig.transFigure, fontsize=25+font_add, color=text_color )
      text_y -= offset_y
  
  if black_background:
    output_dir += 'black_background/'  
  
  figure_name = output_dir + figure_name
  fig.savefig( figure_name, bbox_inches='tight', dpi=400, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )



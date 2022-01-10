import os, sys
import numpy as np
import matplotlib.pylab as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *

import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/fonts/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

legendsize = 12
if system == 'Tornado': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"),  size=legendsize)
if system == 'Eagle': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"),    size=legendsize)
if system == 'xps': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"),      size=legendsize)
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"),        size=legendsize)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legendsize)
if system == 'Mac_mini': prop = None
if system == 'MacBook':  prop = None

figure_width = 8
border_width = 1

tick_size_major, tick_size_minor = 5, 3
tick_label_size_major, tick_label_size_minor = 11, 10
tick_width_major, tick_width_minor = 1.5, 1
label_size = 12
legend_size = 9


# Font Sizes
fontsize_label = 16
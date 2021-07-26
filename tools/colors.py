import pylab
import palettable


# Colors
bright_green = pylab.cm.viridis(.7)
light_blue = pylab.cm.cool(.3)
dark_blue = pylab.cm.viridis(.3) 
dark_purple = pylab.cm.Purples(.7)
blue = 'C0'
orange = 'C1'
green = 'C2'
red = 'C3'
purple = 'C4'
cyan = 'C9' 


cmap_haline = palettable.cmocean.sequential.Haline_10.mpl_colormap
cmap_deep_r = palettable.cmocean.sequential.Deep_20_r.mpl_colormap


haline = palettable.cmocean.sequential.Haline_10_r.mpl_colors
matter = palettable.cmocean.sequential.Matter_20.mpl_colors
colors_1 = palettable.colorbrewer.sequential.PuBu_9.mpl_colors
purples = palettable.colorbrewer.sequential.Purples_9.mpl_colors
yellows = palettable.colorbrewer.sequential.YlOrRd_9.mpl_colors
greens = palettable.colorbrewer.sequential.YlGn_9.mpl_colors 
blues = palettable.colorbrewer.sequential.Blues_9.mpl_colors 
reds = palettable.colorbrewer.sequential.Reds_9.mpl_colors 
yellow_green_blues =  palettable.colorbrewer.sequential.YlGnBu_5.mpl_colors 

light_orange = yellows[3]
dark_green = haline[3]

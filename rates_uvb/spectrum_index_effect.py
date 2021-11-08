import os, sys
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *


# \Delta \alpha = (1 + \alpha + \phi)*( \Delta \Gamma/\Gamma - \Delta H/H )/( 1 + \Delta H/H)

output_dir = home_dir + 'Desktop/'
create_directory( output_dir )

def get_delta_alpha( change_H, change_Gamma,  alpha=-0.5, phi=-3 ):
  delta_alpha = ( alpha + phi + 1  ) * ( change_Gamma - change_H  ) / ( change_H + 1 )
  return delta_alpha
  
  
change_Gamma = -0.4  
change_H = -0.6

delta_alpha = get_delta_alpha( change_H, change_Gamma )


n_samples = 100
change_Gamma_min, change_Gamma_max = -0.8, 0
change_H_min, change_H_max = -0.8, 0
change_Gamma_vals = np.linspace( change_Gamma_min, change_Gamma_max, n_samples )
change_H_vals     = np.linspace( change_H_min, change_H_max, n_samples )


delta_alpha_vals = np.zeros( (n_samples, n_samples ))

for indx_i, change_H in enumerate(change_H_vals):
  for indx_j, change_Gamma in enumerate(change_Gamma_vals):
    if change_Gamma < change_H: continue
    delta_alpha = get_delta_alpha( change_H, change_Gamma )
    delta_alpha_vals[indx_i][indx_j] = delta_alpha
    

ncols, nrows = 1, 1     
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,8*nrows))

im = ax.imshow( delta_alpha_vals, origin='lower', extent=(change_Gamma_min, change_Gamma_max, change_H_min, change_H_max) )
cb = fig.colorbar(im,   )

ax.plot( change_Gamma_vals, change_H_vals, c='k')

figure_name = output_dir + 'delta_alpha_png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


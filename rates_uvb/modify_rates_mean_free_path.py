import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from data_mean_free_path import *

output_dir = data_dir + 'rescale_gamma/mean_free_path/'
create_directory( output_dir )




nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)


z, lambda_vals = data_lambda_P19['z'], data_lambda_P19['lambda']
label = data_lambda_P19['name'] 
ax.plot( z, lambda_vals, label=label )

ax.axvline( x=6, ls='--', lw=1, color='C4' )


z += 0.05
lambda_vals *= 0.78 
label = 'Modified P19' 
ax.plot( z, lambda_vals, label=label )


z = data_lambda_Becker_2021['z']
lambda_vals = data_lambda_Becker_2021['lambda']
delta_h = data_lambda_Becker_2021['delta_h']
delta_l = data_lambda_Becker_2021['delta_l']
label = data_lambda_Becker_2021['name']
ax.errorbar( z, lambda_vals, yerr=[delta_l, delta_h], fmt='o', label=label )



ax.legend( frameon=False, loc=1)

ax.set_yscale('log')

ax.set_ylabel( r'Mean free path at 912 $\AA$ [proper Mpc]'  )
ax.set_xlabel( r'Redshift'  )

ax.set_xlim( 0, 16 )


figure_name = output_dir + 'mean_free_path.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
print( f'Saved Figure: {figure_name}' )
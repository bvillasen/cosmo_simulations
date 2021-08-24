import os, sys
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
import pylab
import matplotlib
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Modify_UVB_Rates, Reaplace_Gamma_Parttial, Load_Grackle_File
from figure_functions import *


  

input_dir  = data_dir + 'rescale_gamma/solution_rescaled_P19/'
output_dir = data_dir + 'rescale_gamma/rescaled_photoionization/'
create_directory( output_dir )





file_name = 'data/UVB_rates_P19m.h5'
uvb_rates = Load_Grackle_File( file_name )
z = uvb_rates['UVBRates']['z']
gamma = uvb_rates['UVBRates']['Chemistry']['k24']


file_name = 'data/CloudyData_UVB_Puchwein2019_cloudy.h5'
uvb_rates_P19 = Load_Grackle_File( file_name )
z_P19 = uvb_rates_P19['UVBRates']['z']
gamma_P19 = uvb_rates_P19['UVBRates']['Chemistry']['k24']

z_P19m = z_P19 + 0.05
gamma_P19m = gamma_P19 * 0.78

# z_new = 


data = np.loadtxt( input_dir + 'rescaled_gamma_rescaled_HI.txt' )
z_rHI, gamma_rHI = data.T 
z_rHI = z_rHI[50:] 
gamma_rHI = gamma_rHI[50:]

change_z = z_rHI[::-1] 
change_gamma = gamma_rHI[::-1]


z_interp = np.linspace( z_P19m.min(), z_P19m.max(), 1000 )
gamma_P19m_interp = 10**( np.interp( z_interp, z_P19m, np.log10(gamma_P19m) )) 

gamma_new = Reaplace_Gamma_Parttial( z_interp, gamma_P19m_interp, change_z, change_gamma )


font_size = 16

ncols, nrows = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))



ax.plot( z_P19,  gamma_P19, lw=2, label='P19' )

ax.plot( z_P19m,  gamma_P19m, lw=2, label='Modified P19' )
# ax.plot( z_r, gamma_r, '--', label='Reconstructed P19-Mod From Equilibrium' )
ax.plot( z_rHI, gamma_rHI, '--', label='From Equilibrium to match rescaled HI' )
ax.plot( z_interp,  gamma_new, lw=1, label='New' )


ax.legend(loc=1, frameon=False, )

ax.set_yscale( 'log' )

ax.set_xlabel(r'$z$', fontsize=font_size )
ax.set_ylabel(r'$\Gamma_{\mathrm{HI}}$', fontsize=font_size )
# 
# ax.axvline( x=6, ls='--', lw=1, color='C4' )
# ax.axvline( x=4.8, ls='--', lw=1, color='C4' )


file_name = output_dir + 'fig_reconstructed_gamma_new.png'
fig.savefig( file_name,  pad_inches=0.1, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
print('Saved Image: ', file_name)


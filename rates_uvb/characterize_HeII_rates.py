import os, sys
import numpy as np
import matplotlib.pylab as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
# import h5py as h5
from tools import *
from uvb_functions import *
from plot_uvb_rates import Plot_UVB_Rates
from figure_functions import *


output_dir = data_dir + 'rescaled_HeII_heating/uvb_rates/'
create_directory( output_dir ) 

# Load the Original Rates
grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
# max_delta_z = 0.1
# grackle_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
# input_rates = Copy_Grakle_UVB_Rates( P19_rates )

parameter_values = { 'scale_He':  0.44,
                     'scale_H':   0.78,
                     'deltaZ_He': 0.27,
                     'deltaZ_H':  0.05 }
                     
# max_delta_z = 0.1
# grackle_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
grackle_data = Modify_Rates_From_Grackle_File( parameter_values, rates_data=grackle_data)

z = grackle_data['UVBRates']['z']
heat_HeII = grackle_data['UVBRates']['Photoheating']['piHeII']
ion_HeII  = grackle_data['UVBRates']['Chemistry']['k25']

fraction = heat_HeII / ion_HeII

zmin, zmax = 4.2, 6.5
indices = ( z > zmin ) * ( z < zmax )
indices = np.where( indices == True )[0]

n =  len( indices )
factor = np.ones(n)


scale_vals = [ 1.0,  0.90,  0.80, 0.7, 0.6, 0.5   ]

# data_heat_HeII = {}
# for indx, val_middle in enumerate( scale_vals ):
#   n_middle = n//2 + 1  
#   factor[:n_middle] *= np.linspace( 1, val_middle, n_middle )
#   n_middle_1 = n_middle 
#   if n_middle % 2 == 0: n_middle_1 -= 1
#   factor[n_middle:] *= np.linspace( val_middle, 1, n_middle_1 )  
#   heat_HeII_new = heat_HeII.copy()
#   heat_HeII_new[indices] *= factor 
#   data_heat_HeII[indx] = { 'scale':val_middle, 'rate':heat_HeII_new }
# 


data_heat_HeII = {}
for indx, val_middle in enumerate( scale_vals ):
  factor *= np.linspace( 1, val_middle, n )
  heat_HeII_new = heat_HeII.copy()
  heat_HeII_new[indices] *= factor 
  data_heat_HeII[indx] = { 'scale':val_middle, 'rate':heat_HeII_new }

for indx, val_middle in enumerate( scale_vals ):
  # Load the Original Rates
  grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
  P19_rates = Load_Grackle_File( grackle_file_name )
  max_delta_z = 0.1
  P19_rates = Extend_Rates_Redshift( max_delta_z, P19_rates )
  input_rates = Copy_Grakle_UVB_Rates(P19_rates)
  P19_mod = Modify_Rates_From_Grackle_File( parameter_values, rates_data=input_rates)
  z = P19_mod['UVBRates']['z']
  heat_HeII = P19_mod['UVBRates']['Photoheating']['piHeII']
  zmin, zmax = 4.2, 6.5
  indices = ( z > zmin ) * ( z < zmax )
  indices = np.where( indices == True )[0]

  n =  len( indices )
  factor = np.ones(n)
  factor *= np.linspace( 1, val_middle, n )
  heat_HeII_new = heat_HeII.copy()
  heat_HeII_new[indices] *= factor 
  P19_mod['UVBRates']['Photoheating']['piHeII'] = heat_HeII_new
  info = f'Modified P19 HeII heating rescaled: {val_middle}' 
  P19_mod['UVBRates']['info'] = info
  file_name = output_dir + f'UVB_rates_{indx}.h5'
  Write_Rates_Grackle_File( file_name, P19_mod )








text_color = 'k'
label_size = 14
figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1



input_dir = data_dir + 'rescaled_HeII_heating/'




ncols, nrows = 1, 1 
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.05, wspace=0.11)



for indx in data_heat_HeII:
  file_name = input_dir + f'solution_{indx}.h5'
  file = h5.File( file_name, 'r' )
  z = file['z'][...]
  temp = file['temperature'][...]
  scale = data_heat_HeII[indx]['scale']
  label = r'$\alpha$ = {0}'.format(scale)
  ax.plot( z, temp, '--', label=label, lw=1  )
  # 

ax.set_xlim( 2, 7 )
ax.set_ylim( 7000, 17000 )
ax.legend( loc=1, frameon=False )

ax.set_xlabel( r'$z$ ', fontsize=label_size )
ax.set_ylabel( r'T [k] ', fontsize=label_size )

figure_name = output_dir + 'temp_evolution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



# ncols, nrows = 1, 1 
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,4*nrows))
# plt.subplots_adjust( hspace = 0.05, wspace=0.11)
# 
# 
# label = 'P19'
# ax.plot( z, fraction, label=label  )
# 
# for indx in data_heat_HeII:
#   scale = data_heat_HeII[indx]['scale']
#   heat_HeII_new = data_heat_HeII[indx]['rate']
#   fraction_new = heat_HeII_new / ion_HeII
#   label = r'$\alpha$ = {0}'.format(scale)
#   ax.plot( z, fraction_new, '--', label=label, lw=1  )
# 
# 
# 
# 
# 
# ax.legend( loc=1, frameon=False )
# ax.axvline( zmin, ls='--', c='C3', lw=1 )
# ax.axvline( zmax, ls='--', c='C3', lw=1 )
# 
# ax.set_xlabel( r'$z$ ', fontsize=label_size )
# ax.set_ylabel( r'HeII Heating / Ionization  Rates ', fontsize=label_size )
# 
# figure_name = output_dir + 'HeII_heat_ion.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 

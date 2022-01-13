import numpy as np
import h5py as h5

in_file_name =  '/Users/bruno/Desktop/Dropbox/Developer/cholla/src/cooling_grackle/CloudyData_UVB_Puchwein2019_cloudy.h5'
in_file_name =  '/Users/bruno/Desktop/uvb_rates_V21_grackle.h5'
out_file_name = '/Users/bruno/Desktop/uvb_rates_V21.txt'

print( f'Loading File: {in_file_name}' )
file = h5.File( in_file_name, 'r' ) 
uvb_rates = file['UVBRates']
z = uvb_rates['z'][...]

# Ionization Rates
ion_HI   = uvb_rates['Chemistry']['k24'][...]
ion_HeI  = uvb_rates['Chemistry']['k26'][...]
ion_HeII = uvb_rates['Chemistry']['k25'][...]

# Heating Rates
heat_HI   = uvb_rates['Photoheating']['piHI'][...]
heat_HeI  = uvb_rates['Photoheating']['piHeI'][...]
heat_HeII = uvb_rates['Photoheating']['piHeII'][...] 

data_out = np.array([ z, ion_HI, heat_HI, ion_HeI, heat_HeI, ion_HeII, heat_HeII ]).T
header = 'z   photoionization_HI   photoheating_HI   photoionization_HeI   photoheating_HeI   photoionization_HeII   photoheating_HeII '
np.savetxt( out_file_name, data_out, header=header )
print( f'Saved File: {out_file_name}')
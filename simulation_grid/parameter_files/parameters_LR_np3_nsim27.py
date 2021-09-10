
# Parameters for changing the H and He Photoionization and Photoheating Rates

param_UVB_Rates = {}

param_UVB_Rates[0] = {}
param_UVB_Rates[0]['key'] = 'A'
param_UVB_Rates[0]['name'] = 'scale_H_ion'
param_UVB_Rates[0]['values'] = [ 0.75,  1.0, 1.25 ]

param_UVB_Rates[1] = {}
param_UVB_Rates[1]['key'] = 'D'
param_UVB_Rates[1]['name'] = 'scale_H_Eheat'
param_UVB_Rates[1]['values'] = [ 0.4, 0.8, 1.2 ]

param_UVB_Rates[2] = {}
param_UVB_Rates[2]['key'] = 'C'
param_UVB_Rates[2]['name'] = 'scale_He_Eheat'
param_UVB_Rates[2]['values'] = [ 0.4, 0.8, 1.2 ]


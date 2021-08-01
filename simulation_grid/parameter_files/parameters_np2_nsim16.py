
# Parameters for changing the H and He Photoionization and Photoheating Rates

param_UVB_Rates = {}

param_UVB_Rates[0] = {}
param_UVB_Rates[0]['key'] = 'A'
param_UVB_Rates[0]['name'] = 'scale_He_heat'
param_UVB_Rates[0]['values'] = [ 0.2,  0.4, 0.6, 0.8 ]

param_UVB_Rates[1] = {}
param_UVB_Rates[1]['key'] = 'B'
param_UVB_Rates[1]['name'] = 'scale_H_heat'
param_UVB_Rates[1]['values'] = [ 0.6, 0.7, 0.8, 0.9 ]


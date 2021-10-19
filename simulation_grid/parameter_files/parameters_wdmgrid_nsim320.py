
# Parameters for changing the H and He Photoionization and Photoheating Rates

param_wdm_UVB_Rates = {}


param_wdm_UVB_Rates[0] = {}
param_wdm_UVB_Rates[0]['key'] = 'A'
param_wdm_UVB_Rates[0]['name'] = 'wdm_mass'
param_wdm_UVB_Rates[0]['values'] = [ 2.0, 3.0, 4.0, 5.0, 6.0 ]

param_wdm_UVB_Rates[1] = {}
param_wdm_UVB_Rates[1]['key'] = 'B'
param_wdm_UVB_Rates[1]['name'] = 'scale_H_ion'
param_wdm_UVB_Rates[1]['values'] = [ 1.0, 1.4, 1.8, 2.2 ]

param_wdm_UVB_Rates[2] = {}
param_wdm_UVB_Rates[2]['key'] = 'C'
param_wdm_UVB_Rates[2]['name'] = 'scale_H_Eheat'
param_wdm_UVB_Rates[2]['values'] = [ 0.1, 0.6, 1.1, 1.6 ]

param_wdm_UVB_Rates[3] = {}
param_wdm_UVB_Rates[3]['key'] = 'D'
param_wdm_UVB_Rates[3]['name'] = 'scale_He_Eheat'
param_wdm_UVB_Rates[3]['values'] = [ 0.2, 0.8, 1.4, 2.0]

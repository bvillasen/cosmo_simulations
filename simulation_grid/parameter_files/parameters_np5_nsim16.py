
# Parameters for changing the H and He Photoionization and Photoheating Rates

param_wdm_UVB_Rates = {}

param_wdm_UVB_Rates[0] = {}
param_wdm_UVB_Rates[0]['key'] = 'A'
param_wdm_UVB_Rates[0]['name'] = 'wdm_mass'
param_wdm_UVB_Rates[0]['values'] = [ 2.0 ]

param_wdm_UVB_Rates[1] = {}
param_wdm_UVB_Rates[1]['key'] = 'B'
param_wdm_UVB_Rates[1]['name'] = 'scale_He'
param_wdm_UVB_Rates[1]['values'] = [ 0.2,  1.0 ]

param_wdm_UVB_Rates[2] = {}
param_wdm_UVB_Rates[2]['key'] = 'C'
param_wdm_UVB_Rates[2]['name'] = 'scale_H'
param_wdm_UVB_Rates[2]['values'] = [ 0.4,  1.2 ]

param_wdm_UVB_Rates[3] = {}
param_wdm_UVB_Rates[3]['key'] = 'D'
param_wdm_UVB_Rates[3]['name'] = 'deltaZ_He'
param_wdm_UVB_Rates[3]['values'] = [ -0.4, 0.6 ]

param_wdm_UVB_Rates[4] = {}
param_wdm_UVB_Rates[4]['key'] = 'E'
param_wdm_UVB_Rates[4]['name'] = 'deltaZ_H'
param_wdm_UVB_Rates[4]['values'] = [ -0.4, 0.4 ]

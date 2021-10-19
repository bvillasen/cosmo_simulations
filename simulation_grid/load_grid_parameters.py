import sys, os
sys.path.append('parameter_files')
from simulation_parameters import grid_name


# Select UVB parameters from file
if grid_name == '1024_np5_nsim16':          from parameters_np5_nsim16 import param_wdm_UVB_Rates as Grid_Parameters
elif grid_name == '1024_P19m_np4_nsim400':  from parameters_P19m_np4_nsim400 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_np2_nsim16':        from parameters_np2_nsim16 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_np4_nsim81':        from parameters_np4_nsim81 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm2p0_nsim8':     from parameters_mwdm2p0_nsim8 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm2p0_nsim64':    from parameters_wdm_nsim64 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm3p0_nsim64':    from parameters_wdm_nsim64 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm4p0_nsim64':    from parameters_wdm_nsim64 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm5p0_nsim64':    from parameters_wdm_nsim64 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_mwdm6p0_nsim64':    from parameters_wdm_nsim64 import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_zreion5p4_nsim27':  from parameters_LR_np3_nsim27  import param_UVB_Rates as Grid_Parameters
elif grid_name == '1024_wdmgrid_nsim192':   from parameters_wdmgrid_nsim192 import param_wdm_UVB_Rates as Grid_Parameters
elif grid_name == '1024_wdmgrid_nsim320':   from parameters_wdmgrid_nsim320 import param_wdm_UVB_Rates as Grid_Parameters
else:
  print( f'Unknokwn grid name: {grid_name}' )
  exit(-1)
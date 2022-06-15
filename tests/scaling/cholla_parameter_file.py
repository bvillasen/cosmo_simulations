


def write_parameter_file( file_name, proc_grid, tile_size, tile_length, 
                          dir_ics, dir_snap, outputs_file, uvb_file ):

  n_procs_x, n_procs_y, n_procs_z = proc_grid
  
  nx = n_procs_x * tile_size
  ny = n_procs_y * tile_size
  nz = n_procs_z * tile_size

  xlen = n_procs_x * tile_length
  ylen = n_procs_y * tile_length
  zlen = n_procs_z * tile_length

  params = f"""# Parameter File for the a Cosmological Simulation.
######################################
nx={nx}
ny={ny}
nz={nz}
tout=1000
outstep=1000
gamma=1.66666667
init=Read_Grid
#Cosmological Parameters
H0=67.66
Omega_M=0.3111
Omega_b=0.0497
Omega_L=0.6889
# domain properties
xmin=0.0
ymin=0.0
zmin=0.0
xlen={xlen}
ylen={ylen}
zlen={zlen}
# type of boundary conditions
xl_bcnd=1
xu_bcnd=1
yl_bcnd=1
yu_bcnd=1
zl_bcnd=1
zu_bcnd=1
nfile=0
tile_length={tile_length}
indir={dir_ics}
outdir={dir_snap}
scale_outputs_file={outputs_file}
UVB_rates_file={uvb_file}
"""
  
  file = open( file_name, 'w' )
  file.write( params )
  file.close()
  print(f'Saved File: {file_name}')
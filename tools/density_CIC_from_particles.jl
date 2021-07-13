using HDF5
current_dir = pwd()
tools_dir = current_dir
push!(LOAD_PATH, tools_dir)
using density_CIC_functions
using Statistics

# Input File
dataDir = "/raid/bruno/data/"
# dataDir = "/home/bruno/Desktop/data/"
# dataDir = "/home/bruno/Desktop/data/"
# dataDir = "/home/bruno/Desktop/ssd_0/data/"
inDir = dataDir * "cosmo_sims/wfirst_1024/snapshots/h5_files/"
outDir = inDir
in_base_name = "snapshot_"
out_base_name = "grid_CIC_"

Lbox = 115e3
const nPoints = 1024

#Domain Parameters
const x_min = 0.0
const y_min = 0.0
const z_min = 0.0
const x_max = Lbox
const y_max = Lbox
const z_max = Lbox
const Lx = x_max - x_min
const Ly = y_max - y_min
const Lz = z_max - z_min

#Grid Properties
const nx = nPoints
const ny = nPoints
const nz = nPoints
const nCells = nx*ny*nz
const dx = Lx / nx
const dy = Ly / ny
const dz = Lz / nz


# #Cells positions in grid ( mid-point )
# c_pos_x = linspace( x_min + dx/2, x_max - dx/2, nx)
# c_pos_y = linspace( y_min + dy/2, y_max - dy/2, ny)
# c_pos_z = linspace( z_min + dz/2, z_max - dz/2, nz)


nSnap = 500

println( "\nSnapshot: $(nSnap)")
snapKey = lpad(nSnap,3,'0')
inFileName = inDir * in_base_name * snapKey * ".h5"

print(" Loading File: $(inFileName)\n")
inFile = h5open( inFileName, "r")


current_a = read( attrs(inFile), "current_a" )
current_z = read( attrs(inFile), "current_z" )
p_mass = read( attrs(inFile), "particle_mass" ) *1e10
print(" Current redshift: $(current_z)\n")
print(" Particle Mass: $(p_mass)  Msun/h\n")
 
print(" Loading pos_x\n")
pos_x = read( inFile, "pos_x" )
print(" Loading pos_y\n")
pos_y = read( inFile, "pos_y" )
print(" Loading pos_z\n")
pos_z = read( inFile, "pos_z" )


nParticles = size( pos_x )[1]
println( "N particles: $(nParticles)")
p_inside = ones( Bool, nParticles )
get_particles_outside_CIC( p_inside, pos_x, pos_y, pos_z, x_min, x_max, y_min, y_max, z_min, z_max, dx, dy, dz  )
# dens = get_interp_CIC( p_inside, field, field, field, pos_x, pos_y, pos_z, nx, ny, nz, x_min, y_min, z_min, x_max, y_max, z_max, dx, dy, dz,  true, true )
dens = get_interp_CIC( p_inside, p_mass, pos_x, pos_y, pos_z, nx, ny, nz, x_min, y_min, z_min, x_max, y_max, z_max, dx, dy, dz, true, true )
dens_avrg = mean(dens)
println( "  Dens mean: $(dens_avrg)")


outFileName = outDir * out_base_name * snapKey * ".h5"
print(" Writing File: $(outFileName)\n")
outFile = h5open( outFileName, "w")
attrs(outFile)["current_a"] = current_a
attrs(outFile)["current_z"] = current_z


outFile["/density"] = dens
close(inFile)
close(outFile)










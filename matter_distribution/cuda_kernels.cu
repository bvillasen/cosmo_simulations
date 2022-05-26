//Get the CIC index from the particle position ( device function )
__device__ void Get_Indexes_CIC( double xMin, double yMin, double zMin, double dx, double dy, double dz, double pos_x, double pos_y, double pos_z, int &indx_x, int &indx_y, int &indx_z ){
  indx_x = (int) floor( ( pos_x - xMin - 0.5*dx ) / dx );
  indx_y = (int) floor( ( pos_y - yMin - 0.5*dy ) / dy );
  indx_z = (int) floor( ( pos_z - zMin - 0.5*dz ) / dz );
}

__device__ double get_weight_tsc_c( double pos, double cell_center, double delta ){
  if ( fabs( (pos - cell_center)/delta ) > 0.5 ) printf( "ERROR: Distance grater than 1/2 in center weight \n");
  return 3./4 - pow( (pos - cell_center)/delta, 2 );
}
__device__ double get_weight_tsc_lr( double pos, double cell_center, double delta ){
  if ( fabs( (pos - cell_center)/delta ) < 0.5  ) printf( "ERROR: Distance lesser than 1/2 in left-right weight \n");
  if ( fabs( (pos - cell_center)/delta ) > 1.5  ) printf( "ERROR: Distance grater than 3/2 in left-right weight \n");
  return 0.5 * pow( 3./2 - fabs(pos - cell_center)/delta, 2 );
}



//Get the CIC index from the particle position ( device function )
__device__ void Get_Indexes_TSC( double xMin, double yMin, double zMin, double dx, double dy, double dz, double pos_x, double pos_y, double pos_z, int &indx_x, int &indx_y, int &indx_z ){
  indx_x = (int) floor( ( pos_x - xMin ) / dx );
  indx_y = (int) floor( ( pos_y - yMin ) / dy );
  indx_z = (int) floor( ( pos_z - zMin ) / dz );
}


extern "C"{
  
  
//CUDA Kernel to compute the TSC density from the particles positions
__global__ void Get_Density_TSC_Kernel( int n_local, double particle_mass,  double *density_dev, 
                                        double *pos_x_dev, double *pos_y_dev, double *pos_z_dev, 
                                        double xMin, double yMin, double zMin, 
                                        double xMax, double yMax, double zMax, 
                                        double dx, double dy, double dz, 
                                        int nx, int ny, int nz, int n_ghost  ){

  int tid = blockIdx.x * blockDim.x + threadIdx.x ;
  if ( tid >= n_local) return;

  int nx_g, ny_g;
  int i, j, k;
  nx_g = nx + 2*n_ghost;
  ny_g = ny + 2*n_ghost;

  double pos_x, pos_y, pos_z, pMass;
  double cell_center_x, cell_center_y, cell_center_z;
  double wx_l, wx_c, wx_r;
  double wy_l, wy_c, wy_r;
  double wz_l, wz_c, wz_r;
  double w, w_sum, wx, wy, wz;
  double dV_inv = 1./(dx*dy*dz);

  pos_x = pos_x_dev[tid];
  pos_y = pos_y_dev[tid];
  pos_z = pos_z_dev[tid];

  pMass = particle_mass * dV_inv;
  
  int indx_x, indx_y, indx_z, indx;
  Get_Indexes_TSC( xMin, yMin, zMin, dx, dy, dz, pos_x, pos_y, pos_z, indx_x, indx_y, indx_z );

  bool in_local = true;

  if ( pos_x < xMin || pos_x >= xMax ) in_local = false;
  if ( pos_y < yMin || pos_y >= yMax ) in_local = false;
  if ( pos_z < zMin || pos_z >= zMax ) in_local = false;
  if ( ! in_local  ) {
    printf(" Density CIC Error: Particle outside local domain [%f  %f  %f]  [%f %f] [%f %f] [%f %f]\n ", pos_x, pos_y, pos_z, xMin, xMax, yMin, yMax, zMin, zMax);
    return;
  }

  cell_center_x = xMin + indx_x*dx + 0.5*dx;
  cell_center_y = yMin + indx_y*dy + 0.5*dy;
  cell_center_z = zMin + indx_z*dz + 0.5*dz;
  
  // if ( tid == 0 ) printf(" d: %f\n", pow( (pos_x - cell_center_x) /dx, 2) );
  
  wx_c = get_weight_tsc_c( pos_x, cell_center_x, dx );
  wy_c = get_weight_tsc_c( pos_y, cell_center_y, dy );
  wz_c = get_weight_tsc_c( pos_z, cell_center_z, dz );
  
  wx_l = get_weight_tsc_lr( pos_x, cell_center_x - dx, dx );
  wy_l = get_weight_tsc_lr( pos_y, cell_center_y - dy, dy );
  wz_l = get_weight_tsc_lr( pos_z, cell_center_z - dz, dz );
  
  wx_r = get_weight_tsc_lr( pos_x, cell_center_x + dx, dx );
  wy_r = get_weight_tsc_lr( pos_y, cell_center_y + dy, dy );
  wz_r = get_weight_tsc_lr( pos_z, cell_center_z + dz, dz );
  
  indx_x += n_ghost;
  indx_y += n_ghost;
  indx_z += n_ghost;
  
  w_sum = 0;
  
  for ( k=-1; k<2; k++ ){
    if ( k == -1 ) wz = wz_l;
    if ( k ==  0 ) wz = wz_c;
    if ( k ==  1 ) wz = wz_r;  
  
    for ( j=-1; j<2; j++ ){
      if ( j == -1 ) wy = wy_l;
      if ( j ==  0 ) wy = wy_c;
      if ( j ==  1 ) wy = wy_r;  
  
      for ( i=-1; i<2; i++ ){
        if ( i == -1 ) wx = wx_l;
        if ( i ==  0 ) wx = wx_c;
        if ( i ==  1 ) wx = wx_r;  
  
        w = wx * wy * wz;
        indx = (indx_x+i) + (indx_y+j)*nx_g + (indx_z+k)*nx_g*ny_g; 
        atomicAdd( &density_dev[indx],  pMass * w );
        w_sum += w;
        // if ( tid == 0 ) printf(" i: %d  j: %d  k: %d   w: %f   w_sum: %f\n", i, j, k,  w, w_sum );  
      }
    }
  }
  
  if ( fabs( w_sum - 1 ) > 1e-4 ) printf("ERROR: Weight sum less than 1.   w_sum: %d", w_sum );
  
}



  
//CUDA Kernel to compute the CIC density from the particles positions
__global__ void Get_Density_CIC_Kernel( int n_local, double particle_mass,  double *density_dev, 
                                        double *pos_x_dev, double *pos_y_dev, double *pos_z_dev, 
                                        double xMin, double yMin, double zMin, 
                                        double xMax, double yMax, double zMax, 
                                        double dx, double dy, double dz, 
                                        int nx, int ny, int nz, int n_ghost  ){

  int tid = blockIdx.x * blockDim.x + threadIdx.x ;
  if ( tid >= n_local) return;

  int nx_g, ny_g;
  nx_g = nx + 2*n_ghost;
  ny_g = ny + 2*n_ghost;

  double pos_x, pos_y, pos_z, pMass;
  double cell_center_x, cell_center_y, cell_center_z;
  double delta_x, delta_y, delta_z;
  double dV_inv = 1./(dx*dy*dz);

  pos_x = pos_x_dev[tid];
  pos_y = pos_y_dev[tid];
  pos_z = pos_z_dev[tid];

  pMass = particle_mass * dV_inv;
  
  int indx_x, indx_y, indx_z, indx;
  Get_Indexes_CIC( xMin, yMin, zMin, dx, dy, dz, pos_x, pos_y, pos_z, indx_x, indx_y, indx_z );

  bool in_local = true;

  if ( pos_x < xMin || pos_x >= xMax ) in_local = false;
  if ( pos_y < yMin || pos_y >= yMax ) in_local = false;
  if ( pos_z < zMin || pos_z >= zMax ) in_local = false;
  if ( ! in_local  ) {
    printf(" Density CIC Error: Particle outside local domain [%f  %f  %f]  [%f %f] [%f %f] [%f %f]\n ", pos_x, pos_y, pos_z, xMin, xMax, yMin, yMax, zMin, zMax);
    return;
  }

  cell_center_x = xMin + indx_x*dx + 0.5*dx;
  cell_center_y = yMin + indx_y*dy + 0.5*dy;
  cell_center_z = zMin + indx_z*dz + 0.5*dz;
  delta_x = 1 - ( pos_x - cell_center_x ) / dx;
  delta_y = 1 - ( pos_y - cell_center_y ) / dy;
  delta_z = 1 - ( pos_z - cell_center_z ) / dz;
  indx_x += n_ghost;
  indx_y += n_ghost;
  indx_z += n_ghost;


  indx = indx_x + indx_y*nx_g + indx_z*nx_g*ny_g;
  // density_dev[indx] += pMass  * delta_x * delta_y * delta_z;
  atomicAdd( &density_dev[indx],  pMass  * delta_x * delta_y * delta_z);

  indx = (indx_x+1) + indx_y*nx_g + indx_z*nx_g*ny_g;
  // density_dev[indx] += pMass  * (1-delta_x) * delta_y * delta_z;
  atomicAdd( &density_dev[indx], pMass  * (1-delta_x) * delta_y * delta_z);

  indx = indx_x + (indx_y+1)*nx_g + indx_z*nx_g*ny_g;
  // density_dev[indx] += pMass  * delta_x * (1-delta_y) * delta_z;
  atomicAdd( &density_dev[indx], pMass  * delta_x * (1-delta_y) * delta_z);
  //
  indx = indx_x + indx_y*nx_g + (indx_z+1)*nx_g*ny_g;
  // density_dev[indx] += pMass  * delta_x * delta_y * (1-delta_z);
  atomicAdd( &density_dev[indx], pMass  * delta_x * delta_y * (1-delta_z) );

  indx = (indx_x+1) + (indx_y+1)*nx_g + indx_z*nx_g*ny_g;
  // density_dev[indx] += pMass  * (1-delta_x) * (1-delta_y) * delta_z;
  atomicAdd( &density_dev[indx], pMass  * (1-delta_x) * (1-delta_y) * delta_z);

  indx = (indx_x+1) + indx_y*nx_g + (indx_z+1)*nx_g*ny_g;
  // density_dev[indx] += pMass  * (1-delta_x) * delta_y * (1-delta_z);
  atomicAdd( &density_dev[indx], pMass  * (1-delta_x) * delta_y * (1-delta_z));

  indx = indx_x + (indx_y+1)*nx_g + (indx_z+1)*nx_g*ny_g;
  // density_dev[indx] += pMass  * delta_x * (1-delta_y) * (1-delta_z);
  atomicAdd( &density_dev[indx], pMass  * delta_x * (1-delta_y) * (1-delta_z));

  indx = (indx_x+1) + (indx_y+1)*nx_g + (indx_z+1)*nx_g*ny_g;
  // density_dev[indx] += pMass * (1-delta_x) * (1-delta_y) * (1-delta_z);
  atomicAdd( &density_dev[indx], pMass * (1-delta_x) * (1-delta_y) * (1-delta_z));

}

}


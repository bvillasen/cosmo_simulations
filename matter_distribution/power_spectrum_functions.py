import numpy as np
import matplotlib.pyplot as plt


def get_delta_k( dens, nx, ny, nz, dx, dy, dz ):
  delta_dens = ( dens - dens.mean() ) / dens.mean()
  FT = np.fft.fftn( delta_dens,  )
  FT2 = FT.real*FT.real + FT.imag*FT.imag
  FT2 = np.fft.fftshift(FT2)
  fft_kx = 2*np.pi*np.fft.fftfreq( nx, d=dx )
  fft_ky = 2*np.pi*np.fft.fftfreq( ny, d=dy )
  fft_kz = 2*np.pi*np.fft.fftfreq( nz, d=dz )
  kx = np.fft.fftshift( fft_kx )
  ky = np.fft.fftshift( fft_ky )
  kz = np.fft.fftshift( fft_kz )
  delta_k2 = FT2
  return delta_k2, kx, ky, kz



def get_delta_k_memory_save( dens, nx, ny, nz, dx, dy, dz ):
  dens_mean = dens.mean()
  dens = ( dens - dens_mean ) / dens_mean
  print('  Computing Fourier Transform')
  FT = np.fft.fftn( dens  )
  print('   Computing FT Magnitude')
  FT = FT.real*FT.real + FT.imag*FT.imag
  print('    Shifting Fourier Transform')
  FT = np.fft.fftshift(FT)
  fft_kx = 2*np.pi*np.fft.fftfreq( nx, d=dx )
  fft_ky = 2*np.pi*np.fft.fftfreq( ny, d=dy )
  fft_kz = 2*np.pi*np.fft.fftfreq( nz, d=dz )
  kx = np.fft.fftshift( fft_kx )
  ky = np.fft.fftshift( fft_ky )
  kz = np.fft.fftshift( fft_kz )
  return FT, kx, ky, kz

def get_power_spectrum(dens, Lbox, nx, ny, nz, dx, dy, dz, n_kSamples=20, n_threads=1 ):
  delta_k2, kx, ky, kz = get_delta_k( dens, nx, ny, nz, dx, dy, dz   )
  # delta_k2, kx, ky, kz = get_delta_k_memory_save( dens, nx, ny, nz, dx, dy, dz, )
  Kz, Ky, Kx = np.meshgrid( kz, ky, kx )
  K_mag = np.sqrt( Kz*Kz + Ky*Ky + Kx*Kx )
  K_mag = K_mag.reshape(K_mag.size)
  delta_k2 = delta_k2.reshape(delta_k2.size)
  k_min = (K_mag[np.where(K_mag>0)]).min() * 0.99
  k_max = K_mag.max()*1.01
  nBins = n_kSamples
  intervals = np.logspace(np.log10(k_min), np.log10(k_max), nBins+1)
  power, bin_edges= np.histogram( K_mag, bins=intervals, weights=delta_k2 )
  n_in_bin, bin_edges = np.histogram( K_mag, bins=intervals )
  n_in_bin = n_in_bin.astype('float')
  bin_centers = np.sqrt(bin_edges[1:] * bin_edges[:-1])
  power = power / n_in_bin / Lbox**3
  indices = n_in_bin > 0
  return power[indices], bin_centers[indices], n_in_bin[indices]

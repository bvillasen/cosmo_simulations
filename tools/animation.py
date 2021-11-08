import sys, time, os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from subprocess import call
from shutil import copyfile
from tools import *

input_dir = data_dir + 'cosmo_sims/rescaled_P19/zero_heat_ion/sim_3/phase_diagram/'

output_dir = home_dir + 'Desktop/'
base_image_name = 'phase_diagram'

out_anim_name = 'phase_diagram_P19m_zero_heat_ion_2'

image_names = [ f for f in os.listdir(input_dir) if f.find(base_image_name) >= 0 and os.path.isfile(input_dir+f) ]
image_names.sort()
n_images = len( image_names )

resize_images = True

resized_dir = input_dir + 'resized/'
create_directory( resized_dir)

start = time.time()
if resize_images:
  print( 'Resizing Images' )
  for i,image_name in enumerate(image_names):
    in_image_name  = input_dir + image_name  
    out_image_name = resized_dir + image_name
    if os.path.isfile( out_image_name ): continue
    in_image = Image.open(in_image_name)
    nx, ny = in_image.size
    nx_out, ny_out = (nx//2)*2, (ny//2)*2
    out_image = in_image.resize(( nx_out, ny_out ))
    out_image.save(out_image_name)
    print_progress( i+1, n_images, start ) 
  input_dir = resized_dir


start_frame = 0
frame_rate = 2


cmd = f'ffmpeg -framerate {frame_rate} -start_number {start_frame}  '
# cmd += ' -start_number 20'
cmd += ' -i {0}{1}_%d.png '.format( input_dir, base_image_name )
cmd += ' -pix_fmt yuv420p '
cmd += ' -vcodec libx264 '
# cmd += '-b 9100k '
cmd += '{0}{1}.mp4'.format( output_dir, out_anim_name )
# cmd += ' -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'
# cmd += ' -vf pad="width=ceil(iw/2)*2:height=ceil(ih/2)*2"'
cmd += ' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"'
print( f'Running Command: {cmd}')
time.sleep(2)
os.system( cmd )



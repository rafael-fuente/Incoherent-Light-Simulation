import meep as mp
import h5py
import os
from pathlib import Path
import numpy as np
from light_sources import *

#create and run the simulation. All lengths are measured in micrometers (μm)
def double_slit_simulation(light_source, 
                           extent,
                           aperture_width,
                           aperture_depth,
                           aperture_distance,
                           aperture_separation,
                           pixels_per_wavelength,
                           total_femtoseconds,
                           number_of_frames,
                           complex_average,
                           simulation_name):
    
    
    femtoseconds_per_frame = total_femtoseconds/number_of_frames
    
    center=mp.Vector3((extent[1]+ extent[0])/2,   (extent[2]+ extent[3])/2)
    cell = mp.Vector3(extent[1]- extent[0] ,extent[2]- extent[3],0)
    
    #simulation boundary (PML = perfectly matched absorbing layers)
    pml_layers = [mp.PML(1)]

    #light sources
    sources = light_source.get_meep_sources(center)


    block_length = ((extent[2]- extent[3]) - 2*aperture_width - aperture_separation)/2

    # create the double slit geometry
    geometry = [mp.Block(mp.Vector3(aperture_depth, block_length, mp.inf),
                         center=mp.Vector3(aperture_distance- center.x, extent[2]  - block_length / 2.  ,0),
                         material=mp.Medium(epsilon=9999)),

                mp.Block(mp.Vector3(aperture_depth, block_length, mp.inf),
                          center=mp.Vector3(aperture_distance- center.x, extent[3]  + block_length / 2.  ,0),
                          material=mp.Medium(epsilon=9999)),

                mp.Block(mp.Vector3(aperture_depth, aperture_separation, mp.inf),
                          center=mp.Vector3(aperture_distance- center.x,0  ,0),
                          material=mp.Medium(epsilon=9999)),         

               ]


    pixels_per_um = pixels_per_wavelength / light_source.λ



    sim = mp.Simulation(cell_size=cell,
                        sources=sources,
                        boundary_layers=pml_layers,
                        geometry = geometry,
                        resolution=pixels_per_um,
                       force_complex_fields = complex_average)


    if os.path.exists(Path(simulation_name)):
        os.remove(Path(simulation_name))

    with h5py.File(simulation_name, 'a') as f:
        
        #run simulation and store it in a hdf5 file.
        sim.run(until=  femtoseconds_per_frame *  3. / 10 )
        ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
        eps_data = sim.get_array(center=mp.Vector3(0,0,0), size=cell, component=mp.Dielectric)    
        Sx_data = sim.get_array(center=mp.Vector3(0,0,0), size=cell, component=mp.Sx)


        dset = f.create_dataset('Ez', (number_of_frames,*ez_data.shape) ,dtype='float64', maxshape=(None, *ez_data.shape))
        dset = f.create_dataset('eps_data', eps_data.shape ,dtype='float64', maxshape=eps_data.shape)
        dset = f.create_dataset('Sx', (number_of_frames,*Sx_data.shape) ,dtype='float64', maxshape=(None, *Sx_data.shape))
        
        
        
        f.attrs['cell_x'] = cell.x
        f.attrs['cell_y'] = cell.y
        f.attrs['extent'] = np.array(extent)
        f.attrs['total_femtoseconds'] = total_femtoseconds
        f.attrs['number_of_frames'] = number_of_frames
        
        f.attrs['simulated_femtoseconds'] = femtoseconds_per_frame
        f.attrs['simulated_frames'] = 1
        

    
        f['eps_data'][:] = eps_data
        absEz = np.abs(ez_data)
        f['Ez'][0] = absEz
        f['Sx'][0] = Sx_data
        f['max_Ez_value'] = np.amax(absEz)
        
        
        # frame loop
        for i in range(1,number_of_frames):
            #print(i)
            sim.run(until=  femtoseconds_per_frame *  3. / 10 )
            ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
            Sx_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Sx)

            f['Ez'][i]  = np.abs(ez_data)
            f['Sx'][i] = Sx_data
            
            current_max_Ez = np.amax(absEz)
            if f['max_Ez_value'] < current_max_Ez:
                f['max_Ez_value'] = current_max_Ez

            f.attrs['simulated_femtoseconds'] += femtoseconds_per_frame
            f.attrs['simulated_frames'] += 1


            



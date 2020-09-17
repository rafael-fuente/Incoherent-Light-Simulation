import meep as mp
import h5py
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from light_sources import *

#create and run the simulation. All lengths are measured in micrometers (μm)
def double_slit_simulation(light_source, 
                           rang,
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
    
    center=mp.Vector3((rang[1]+ rang[0])/2,   (rang[2]+ rang[3])/2)
    cell = mp.Vector3(rang[1]- rang[0] ,rang[2]- rang[3],0)
    
    #simulation boundary (PML = perfectly matched absorbing layers)
    pml_layers = [mp.PML(1)]

    #light sources
    sources = light_source.get_meep_sources(center)


    block_length = ((rang[2]- rang[3]) - 2*aperture_width - aperture_separation)/2

    # create the double slit geometry
    geometry = [mp.Block(mp.Vector3(aperture_depth, block_length, mp.inf),
                         center=mp.Vector3(aperture_distance- center.x, rang[2]  - block_length / 2.  ,0),
                         material=mp.Medium(epsilon=9999)),

                mp.Block(mp.Vector3(aperture_depth, block_length, mp.inf),
                          center=mp.Vector3(aperture_distance- center.x, rang[3]  + block_length / 2.  ,0),
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
        f.attrs['rang'] = np.array(rang)
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
            print(i)
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


            


            
# visualize simulation with matplotlib. It uses a slider to change the time
def visualize(simulation_name, color_saturation_factor):
    with h5py.File(simulation_name, 'a') as f:
        
        cell_x = f.attrs['cell_x'] 
        cell_y = f.attrs['cell_y'] 
        rang = f.attrs['rang'] 
        total_femtoseconds = f.attrs['total_femtoseconds'] 
        number_of_frames = f.attrs['number_of_frames'] 
        max_Ez_value = f['max_Ez_value'][()]

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(10.0, 5.0))
        ax = fig.add_subplot(1,1,1)  
        plt.subplots_adjust(bottom=0.2,left=0.15)

        Ez_data = f['Ez'][0][:]
        eps_data = f['eps_data'][:]

        # plot the double slit
        ax.imshow(eps_data.transpose(), interpolation='spline36', cmap='bone', alpha=1, extent = rang)

        # plot the field
        im = ax.imshow(np.abs(Ez_data.T), interpolation='spline36', cmap='inferno', alpha=0.9, extent = rang, vmax = max_Ez_value*color_saturation_factor)
        ax.set_xlabel('Y [μm]')
        ax.set_ylabel('X [μm]')


        def update(t):

            ax.clear()
            index = int(np.round((t / total_femtoseconds * number_of_frames)))
            
            Ez_data = f['Ez'][index][:]
            eps_data = f['eps_data'][:]

            # plot the double slit
            ax.imshow(eps_data.transpose(), interpolation='spline36', cmap='bone', alpha=1, extent = rang)

            # plot the field
            im = ax.imshow(np.abs(Ez_data.T), interpolation='spline36', cmap='inferno', alpha=0.9, extent = rang, vmax = max_Ez_value*color_saturation_factor)
            ax.set_xlabel('Y [μm]')
            ax.set_ylabel('X [μm]')

        from matplotlib.widgets import Slider

        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
        slider = Slider(slider_ax,      # the axes object containing the slider
                          't',            # the name of the slider parameter
                          0,          # minimal value of the parameter
                          total_femtoseconds,          # maximal value of the parameter
                          valinit=0,  # initial value of the parameter 
                          color = '#5c05ff' 
                         )

        slider.on_changed(update)
        plt.show() 


import numpy as np
import h5py
import matplotlib.pyplot as plt

# Visualize simulation stored in a hdf5 file with matplotlib. 
# It uses a slider to change the time
def visualize(simulation_name, max_colormap_factor = 1.):
    with h5py.File(simulation_name, 'a') as f:
        
        cell_x = f.attrs['cell_x'] 
        cell_y = f.attrs['cell_y'] 
        extent = f.attrs['extent'] 
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
        ax.imshow(eps_data.transpose(), interpolation='spline36', cmap='bone', alpha=1, extent = extent)

        # plot the field
        im = ax.imshow(np.abs(Ez_data.T), interpolation='spline36', cmap='inferno', alpha=0.9, extent = extent, vmax = max_Ez_value*max_colormap_factor)
        ax.set_xlabel('Y [μm]')
        ax.set_ylabel('X [μm]')


        def update(t):

            ax.clear()
            index = int(np.round((t / total_femtoseconds * (number_of_frames-1))))
            
            Ez_data = f['Ez'][index][:]
            eps_data = f['eps_data'][:]

            # plot the double slit
            ax.imshow(eps_data.transpose(), interpolation='spline36', cmap='bone', alpha=1, extent = extent)

            # plot the field
            im = ax.imshow(np.abs(Ez_data.T), interpolation='spline36', cmap='inferno', alpha=0.9, extent = extent, vmax = max_Ez_value*max_colormap_factor)
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


from source_simulator import *
import numpy as np
from vector3 import *

nm = 1e-9
um = 1e-6


def random_in_unit_disk(size):
    """generates random vectors uniformly distributed inside a circle"""
    r = np.sqrt(np.random.rand(size))
    phi = np.random.rand(size)*2*np.pi
    return r * np.cos(phi), r * np.sin(phi)


def random_sources_in_disk(size, power, wavelength_mean, bandwidth,  r):
    """generates random point sorces with random phases uniformly distributed inside a circle"""
    source_list = [None]*size
    x0, y0 = random_in_unit_disk(size)
    x0, y0 = r*x0,r*y0
    phase = np.random.rand(size)* 2*np.pi
    wavelength =  wavelength_mean + bandwidth*(np.random.rand(size)-0.5)

    for i in range(size):
        source_list[i] = Source(power = 1, λ = wavelength[i], phase = phase[i], pos = vec3(x0[i],y0[i],0))

    return source_list


N =30 # number of point sources

#coherence time : 1/ ((3*1e8)/(650 * nm) - (3*1e8)/(651 * nm)) = 1.4𝑒−12


sim = Source_system( random_sources_in_disk(N,power = 1, wavelength_mean = 650 * nm , bandwidth = 1.0 * nm, r = 2.0* um  ))

#complex average makes convergence faster.
#sim.visualize_field_in_xy_plane(grid_divisions = 150, rang = [-10* um,10* um,-10* um,10* um], vmin = 0, vmax = np.sqrt(N/( (5*um)**2)) ,  timescale = 1e-8, lengthscale = um, time_average_size = 100, number_of_samples = 1000)
#sim.visualize_field_in_xy_plane(grid_divisions = 150, rang = [-10* um,10* um,-10* um,10* um], vmin = 0, vmax = np.sqrt(N/( (5*um)**2)) ,  timescale = 1e-10, lengthscale = um, time_average_size = 100, number_of_samples = 1000)


sim.visualize_field_in_xy_plane(grid_divisions = 150
                                        , rang = [-10* um,10* um,-10* um,10* um],  # grid  size
                                        vmin = 0, vmax = np.sqrt(N/( (5*um)**2)),  # matplotlib imshow parameter:  data range that the colormap covers
                                        number_of_samples = 1000, #for this example, you are going to need a lot of samples to converge to the solution. 
                                        time_average_size = 0.01,
                                        timescale = 1e-6, # order of magnitude of the simulation time  
                                        lengthscale = um,  # order of magnitude of the grid
                                        complex_average = True # makes convergence of the integration faster
                                        )

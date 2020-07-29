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
    """generates random point sorces with random phases and wavelengths uniformly distributed inside a circle"""
    source_list = [None]*size
    x0, y0 = random_in_unit_disk(size)
    x0, y0 = r*x0,r*y0
    phase = np.random.rand(size)* 2*np.pi
    wavelength =  wavelength_mean + bandwidth*(np.random.rand(size)-0.5)

    for i in range(size):
        source_list[i] = Source(power = 1, λ = wavelength[i], phase = phase[i], pos = vec3(x0[i],y0[i],0))

    return source_list


N =30 # number of point sources



sim = Source_system( random_sources_in_disk(N,power = 1, wavelength_mean = 650 * nm , bandwidth = 1.0 * nm, r = 2.0* um  ))


sim.dynamic_visualize_field_in_xy_plane(grid_divisions = 150
                                        , rang = [-7* um,7* um,-7* um,7* um],  # grid  size
                                        vmin = 0, vmax = np.sqrt(N/( (3*um)**2)),  # matplotlib imshow parameter:  data range that the colormap covers
                                        number_of_samples = 10, 
                                        max_time = 50, timescale = 1e-16, # order of magnitude of the simulation time  
                                        lengthscale = um,  # order of magnitude of the grid
                                        )

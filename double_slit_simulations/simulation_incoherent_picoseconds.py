import numpy as np
from double_slit_simulator import *
from visualization import *


double_slit_simulation(light_source = Incoherent_rectangular_source(number_of_dipoles = 10000, 
                                                                    position = mp.Vector3(1,0,0),
                                                                    λ=0.65 , bandwidth=0.01, 
                                                                    width = 2, height = 10),
                       extent = [0,60 , 15, -15],
                       aperture_width = 2.,
                       aperture_depth = 0.5,
                       aperture_distance = 30,
                       aperture_separation = 3,
                       pixels_per_wavelength = 10,
                       total_femtoseconds = 20000, #20 picoseconds
                       number_of_frames = 50,
                       complex_average = True,
                       simulation_name = "simulation_incoherent_picoseconds.h5")

visualize(simulation_name = "simulation_incoherent_picoseconds.h5",
		      max_colormap_factor = 0.5)

from double_slit_simulator import *
from visualization import *


double_slit_simulation(light_source = Gaussian_source(position = mp.Vector3(1,0,0),
                                                      direction = mp.Vector3(1,0,0),
                                                      λ=0.65,
                                                      beam_width = 11),
                       extent = [0,60 , 15, -15],
                       aperture_width = 2.,
                       aperture_depth = 0.5,
                       aperture_distance = 30,
                       aperture_separation = 3,
                       pixels_per_wavelength = 10,
                       total_femtoseconds = 300,
                       number_of_frames = 50,
                       complex_average = False,
                       simulation_name = "simulation_coherent_femtoseconds.h5")

visualize(simulation_name = "simulation_coherent_femtoseconds.h5",
		      max_colormap_factor = 1.)

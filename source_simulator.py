import numpy as np
import matplotlib.pyplot as plt
import time
import progressbar


from vector3 import *

nm = 1e-9
um = 1e-6



class Source:
    def __init__(self, power,λ, phase, pos):
        self.power=power
        self.λ=λ
        self.pos=pos
        self.phase=phase

        

        

class Source_system:

    
    def __init__(self, source_list = []):

        self.c = 3 * 1e8
        
        self.source_list = source_list
        


    def dynamic_visualize_field_in_xy_plane(self, grid_divisions, rang = [0,30,-30,30], max_time = 5, time_average_size = 0.01, vmin = None, vmax = None,  number_of_samples = 1, timescale = 1e-12,   lengthscale = 1e-1, complex_average = False):   

        

        x = np.linspace(rang[0],rang[1], grid_divisions)
        y = np.linspace(rang[2],rang[3], grid_divisions)
        x,y = np.meshgrid(x,y)
        
        r = vec3(x,y,0)


        scaled_rang = [rang[0]/lengthscale, rang[1]/lengthscale, rang[2]/lengthscale, rang[3]/lengthscale]



        plt.style.use('dark_background')
        fig = plt.figure(figsize=(5.0, 5.0))

        
        ax = fig.add_subplot(1,1,1)  
        plt.subplots_adjust(bottom=0.2,left=0.15)


        def update(t):

            ax.clear()

            ax.set_xlabel('X')
            ax.set_ylabel('Y')

            
            t0 = time.time()
            
            #total sqare root intensity
            intensity = 0

            for j in range(number_of_samples):


                r_sample =  vec3(r.x + 1.*(np.random.rand(grid_divisions, grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                                 r.y + 1.*(np.random.rand(grid_divisions, grid_divisions))* (rang[3]-rang[2])  /(grid_divisions)  ,  0.)
                E_sample = 0.

                t_sample = t +  1*time_average_size   * np.random.rand(1)

                for source in self.source_list:

                    r_mod = (r_sample - source.pos ).length() 
                    f = ((self.c*timescale) /source.λ)

                    if complex_average == False:

                        E_source = source.power * np.cos(   (2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod

                    else:

                        E_source = source.power * np.exp(   1j*(2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod


                    E_sample += E_source

                #Field is proportionally to the squared module of electric field. Square root is represented to emphasize interferences.
                if complex_average == False:
                    intensity += (E_sample*E_sample)/number_of_samples
                else:
                    intensity += (np.real(E_sample*np.conjugate(E_sample))/2.)/number_of_samples

            #ax.set_title("Took "+ str(time.time() - t0))  
            im = ax.imshow(np.sqrt(intensity), extent = scaled_rang, origin='lower',  alpha=0.8, vmin = vmin, vmax = vmax, cmap=plt.cm.inferno, aspect='equal', interpolation = 'bilinear')
                
        from matplotlib.widgets import Slider

        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
        slider = Slider(slider_ax,      # the axes object containing the slider
                          't',            # the name of the slider parameter
                          0,          # minimal value of the parameter
                          max_time,          # maximal value of the parameter
                          valinit=0,  # initial value of the parameter 
                          color = '#5c05ff' 
                         )

        slider.on_changed(update)
        plt.show() 


    def visualize_field_in_xy_plane(self, grid_divisions, rang = [0,30,-30,30], time_average_size = 0.01, vmin = 0, vmax = None,  number_of_samples = 1, timescale = 1e-12,   lengthscale = 1e-1, complex_average = False):   

        x = np.linspace(rang[0],rang[1], grid_divisions)
        y = np.linspace(rang[2],rang[3], grid_divisions)
        x,y = np.meshgrid(x,y)
        
        r = vec3(x,y,0)


        scaled_rang = [rang[0]/lengthscale, rang[1]/lengthscale, rang[2]/lengthscale, rang[3]/lengthscale]






        
        t_rand = np.random.rand(number_of_samples)
        
        #total sqare root intensity
        intensity = 0
        bar = progressbar.ProgressBar()
        for j in bar(range(number_of_samples)):


            r_sample =  vec3(r.x + 1.*(np.random.rand(grid_divisions, grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                             r.y + 1.*(np.random.rand(grid_divisions, grid_divisions))* (rang[3]-rang[2])  /(grid_divisions)  ,  0.)
            E_sample = 0.

            t_sample = time_average_size   * t_rand[j]

            for source in self.source_list:

                r_mod = (r_sample - source.pos ).length() 
                f = ((self.c*timescale) /source.λ)
                if complex_average == False:

                    E_source = source.power * np.cos(   (2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod

                else:

                    E_source = source.power * np.exp(   1j*(2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod


                E_sample += E_source

            #Field is proportionally to the squared module of electric field. Square root of intesity is represented to emphasize interferences.
            if complex_average == False:
                intensity += (E_sample*E_sample)/number_of_samples
            else:
                intensity += (np.real(E_sample*np.conjugate(E_sample))/2.)/number_of_samples

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(5.0, 5.0))


        ax = fig.add_subplot(1,1,1)  
        plt.subplots_adjust(bottom=0.2,left=0.15)



        ax.clear()

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        im = ax.imshow(np.sqrt(intensity), extent = scaled_rang, origin='lower',  alpha=0.8, vmin = vmin, vmax = vmax, cmap=plt.cm.inferno, aspect='equal', interpolation = 'bilinear')
        plt.show() 


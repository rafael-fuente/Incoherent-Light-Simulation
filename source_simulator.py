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


                r_sample =  vec3(r.x + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                                 r.y + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[3]-rang[2])  /(grid_divisions)  ,  0.)
                E_sample = 0.

                t_sample = t +  0*time_average_size   * np.random.rand(1)

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

        t0 = time.time()

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
        print ("Took", time.time() - t0)
        plt.show() 


    def visualize_field_in_x(self, grid_divisions, rang = [0,30], time_average_size = 0.01,   number_of_samples = 1, timescale = 1e-12,   lengthscale = 1e-1, complex_average = False):   

        t0 = time.time()

        x = np.linspace(rang[0],rang[1], grid_divisions)
        
        r = vec3(x,0,0)


        scaled_rang = [rang[0]/lengthscale, rang[1]/lengthscale]






        
        t_rand = np.random.rand(number_of_samples)
        
        #total sqare root intensity
        intensity = 0
        intensity2 = 0
        bar = progressbar.ProgressBar()
        for j in range(number_of_samples):


            r_sample =  vec3(r.x + 1.*(np.random.rand(grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                            0. ,  0.)
            E_sample = 0.
            I_sample = 0
            t_sample = 0 +  1.*time_average_size   * t_rand[j]

            for source in self.source_list:

                r_mod = (r_sample - source.pos ).length() 
                f = ((self.c*timescale) /source.λ)
                if complex_average == False:

                    E_source = source.power * np.cos(   (2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod
                    I_source = (source.power**2  / (r_mod)**2)/2.
                else:

                    E_source = source.power * np.exp(   1j*(2*np.pi*(-r_mod /source.λ)  + source.phase  +  2*np.pi* f * t_sample     )) / r_mod
                    I_source = (source.power**2  / (r_mod)**2)/2.

                E_sample += E_source
                I_sample += I_source
            #Field is proportionally to the squared module of electric field. Square root is represented to emphasize interferences.
            if complex_average == False:
                intensity += E_sample*E_sample/number_of_samples
                intensity2 += (I_sample)/number_of_samples #*0.90

            else:
                intensity += (np.real(E_sample*np.conjugate(E_sample))/2.)/number_of_samples
                intensity2 += (I_sample)/number_of_samples #*0.90
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(5.0, 5.0))


        ax = fig.add_subplot(1,1,1)  
        plt.subplots_adjust(bottom=0.2,left=0.15)



        ax.clear()

        ax.set_xlabel('X')
        
        im = ax.plot(x, np.sqrt(intensity),label="E")
        im = ax.plot(x, np.sqrt(intensity2),label="I")
        ax.legend(loc ="upper right")
        print ("Took", time.time() - t0)
        plt.show() 




    def image_gen(self,real_max_time, max_time, grid_divisions, rang = [0,30,-30,30], time_average_size = 0.01, vmin = 0, vmax = None,  number_of_samples = 1, timescale = 1e-12,   lengthscale = 1e-1, complex_average = False):   

        fps = 60
        number_of_frames = int(fps*(real_max_time - 0))
        print(number_of_frames)
        dt = (max_time - 0)/number_of_frames

        t = 0

        from pathlib import Path

        try:
            Path("./frames").mkdir()

        except FileExistsError:
            pass

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(7.2, 7.2))
        ax = fig.add_subplot(1,1,1)  
        for i in range(number_of_frames):

            t0 = time.time()

            x = np.linspace(rang[0],rang[1], grid_divisions)
            y = np.linspace(rang[2],rang[3], grid_divisions)
            x,y = np.meshgrid(x,y)
            
            r = vec3(x,y,0)


            scaled_rang = [rang[0]/lengthscale, rang[1]/lengthscale, rang[2]/lengthscale, rang[3]/lengthscale]






            
            t_rand = np.random.rand(number_of_samples)
            
            #total sqare root intensity
            intensity = 0
            
            for j in range(number_of_samples):


                r_sample =  vec3(r.x + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                                 r.y + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[3]-rang[2])  /(grid_divisions)  ,  0.)
                E_sample = 0.

                t_sample = t +  0.*time_average_size   * t_rand[j]

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
                    intensity += np.abs(E_sample)/number_of_samples
                else:
                    intensity += np.sqrt(np.real(E_sample*np.conjugate(E_sample))/2.)/number_of_samples



            

            
            ax.clear()


            rounded_time = "%.2f" % round(t, 2)
            ax.set_title("t = " + rounded_time + " picoseconds")

            ax.set_xlabel('X [μm]')
            ax.set_ylabel('Y [μm]')
            im = ax.imshow(intensity, extent = scaled_rang, origin='lower',  alpha=0.8, vmin = vmin, vmax = vmax, cmap=plt.cm.inferno, aspect='equal', interpolation = 'bilinear')
            print ("Took", time.time() - t0)
            fig.savefig('frames/sim_'+str(i)+'.png')

            t += dt










    def intensity_image_gen(self,real_max_time, max_time, grid_divisions, rang = [0,30,-30,30], time_average_size = 0.01, vmin = 0, vmax = None,  number_of_samples = 1, timescale = 1e-12,   lengthscale = 1e-1, complex_average = False):   

        fps = 60
        number_of_frames = int(fps*(real_max_time - 0))
        print(number_of_frames)
        dt = (max_time - 0)/number_of_frames

        t = 0

        from pathlib import Path

        try:
            Path("./frames").mkdir()

        except FileExistsError:
            pass

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(7.2, 7.2))
        ax = fig.add_subplot(1,1,1)  
        for i in range(number_of_frames):

            t0 = time.time()

            x = np.linspace(rang[0],rang[1], grid_divisions)
            y = np.linspace(rang[2],rang[3], grid_divisions)
            x,y = np.meshgrid(x,y)
            
            r = vec3(x,y,0)


            scaled_rang = [rang[0]/lengthscale, rang[1]/lengthscale, rang[2]/lengthscale, rang[3]/lengthscale]






            
            t_rand = np.random.rand(number_of_samples)
            
            #total sqare root intensity
            intensity = 0
            
            for j in range(number_of_samples):


                r_sample =  vec3(r.x + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[1]-rang[0])  /(grid_divisions),
                                 r.y + 0.*(np.random.rand(grid_divisions, grid_divisions))* (rang[3]-rang[2])  /(grid_divisions)  ,  0.)
                E_sample = 0.

                t_sample = t +  0.*time_average_size   * t_rand[j]

                for source in self.source_list:

                    r_mod = (r_sample - source.pos ).length() 
                    f = ((self.c*timescale) /source.λ)

                    I_source = (source.power**2  / (r_mod)**2)/2.


                    E_sample += I_source

                #Field is proportionally to the squared module of electric field. Square root is represented to emphasize interferences.
                intensity += (E_sample)/number_of_samples #*0.90



            

            
            ax.clear()

            print(t)
            rounded_time = "%.2f" % round(t, 2)
            ax.set_title("t = " + rounded_time + " microseconds")

            ax.set_xlabel('X [μm]')
            ax.set_ylabel('Y [μm]')
            im = ax.imshow(np.sqrt(intensity), extent = scaled_rang, origin='lower',  alpha=0.8, vmin = vmin, vmax = vmax, cmap=plt.cm.inferno, aspect='equal', interpolation = 'bilinear')
            print ("Took", time.time() - t0)
            fig.savefig('frames/sim_'+str(i)+'.png')

            t += dt
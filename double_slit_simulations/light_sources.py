from abc import abstractmethod 
import meep as mp
import numpy as np

class Light_source:
    def __init__(self, position):
        self.position = position
        
    @abstractmethod   
    def get_meep_sources(self):
        pass



class Gaussian_source(Light_source):
    def __init__(self, position, direction, λ, beam_width):
        
        self.position = position
        self.direction = direction
        self.λ = λ
        self.w0 = beam_width/2
        
    def get_meep_sources(self, sim_center):

        def _gaussian_beam(x):
            return np.exp(1j*2*np.pi* 2*np.pi/self.λ * self.direction.dot(x-self.position+sim_center)  -  (x-self.position+sim_center).dot(x-self.position+sim_center)/(2*self.w0**2))

        
        source_list = [mp.Source(src=mp.ContinuousSource(1/self.λ),
                         component=mp.Ez,
                         center= self.position - sim_center,
                         size=mp.Vector3(-self.direction.y,self.direction.x,0)*30,
                         amp_func=_gaussian_beam)]

        return source_list


class Incoherent_rectangular_source(Light_source):
    def __init__(self, number_of_dipoles, position,
                λ, bandwidth, width, height):
        
        self.number_of_dipoles = number_of_dipoles
        self.position = position
        self.bandwidth = bandwidth
        self.λ = λ
        self.width = width
        self.height = height
        
        self.y0 = (np.random.rand(number_of_dipoles)-0.5)*height
        self.x0 = (np.random.rand(number_of_dipoles)-0.5)*width
        self.phase = np.random.rand(number_of_dipoles)* 2*np.pi
        self.wavelength =  λ + bandwidth*(np.random.rand(number_of_dipoles)-0.5)
        
    def get_meep_sources(self, sim_center):
        
        source_list = [None]*self.number_of_dipoles

        for i in range(self.number_of_dipoles):
            source_list[i] = mp.Source(mp.ContinuousSource(frequency=1/self.λ),
                             component=mp.Ez,
                             center= self.position - sim_center +  mp.Vector3(self.x0[i], self.y0[i]))


        return source_list


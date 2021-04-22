# Incoherent-Light-Simulation

This is a research project with the goal of illustrating the concept of spatial coherence in light. 
The incoherent light propagation is simulated through three different time scales. As the time scales goes up and the field is averaged, the visibility of the interferences disappears, yielding a uniform distribution.

## How the simulations are done

This simulations works computing the field created by point sources with random phases and randomly placed inside a the light source dimensions.

Time averaging is done using Monte Carlo integration. 

Then, the simulation is represented and animated with matplotlib.

Check the [video](https://www.youtube.com/watch?v=ySte6NRuA-k&list=PLYkZehxPE_IhJDMTJUob1ZbxWhL8AjHDi&index=1
) and the [article](https://rafael-fuente.github.io/visual-explanation-of-the-van-cittert-zernike-theorem-the-double-slit-experiment-with-incoherent-and-coherent-light.html) for further explanation.


## Installation

Just clone or download the repository. The package requeriments are:

1. numpy
2. matplotlib
3. progressbar

## Simulations

To perform the simulations, just run from the command prompt the corresponding Python scripts:

```
python simulation_femtoseconds.py
```

[![animation](/images/femtoseconds_sim.gif)](/simulation_femtoseconds.py)


```
python simulation_picoseconds.py
```

[![animation](/images/picoseconds_sim.gif)](/simulation_picoseconds.py)


```
python simulation_microseconds.py
```

[![animation](/images/microseconds_sim.gif)](/simulation_microseconds.py)


There are more simulations, implemented with a FDTD scheme:

[Simulations of the double slit experiment with incoherent and coherent light.](/double_slit_simulations)

They illustrate the concept of spatial coherence further, showing the differences with spatially coherent light and how the visibility of the interferences varies as the distance from the double slit to the light source increases.
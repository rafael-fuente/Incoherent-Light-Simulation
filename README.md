# Incoherent-Light-Simulation
[![DOI](https://zenodo.org/badge/282254555.svg)](https://zenodo.org/badge/latestdoi/282254555)

This is a project that consists of a compilation of educative optical simulations with the goal of illustrating the concept of spatial coherence.

The simulations focus on visualizing the differences between the behavior of incoherent and coherent light propagation through different time scales: femtoseconds, picoseconds, and microseconds. When the time scale goes up and the field is averaged, the interferometric visibility of the fringes disappears, yielding a uniform distribution.


## How the simulations are done

These simulations are performed by computing the field created by point sources with random phases and randomly placed inside the light source dimensions.

Time averaging is done using Monte Carlo integration. 

Then, the simulation is represented and animated with matplotlib.

Check the [video](https://www.youtube.com/watch?v=ySte6NRuA-k&list=PLYkZehxPE_IhJDMTJUob1ZbxWhL8AjHDi&index=1
) for the demonstration and the [article](https://rafael-fuente.github.io/visual-explanation-of-the-van-cittert-zernike-theorem-the-double-slit-experiment-with-incoherent-and-coherent-light.html) for further explanation.


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


The double slit experiment finite-difference time-domain (FDTD) simulations reproduce the results of the Van-Cittert-Zernike theorem, showing how the interferometric visibility of the fringes varies due to the different parameters of the simulation.

[Simulations of the double slit experiment with incoherent and coherent light.](/double_slit_simulations)
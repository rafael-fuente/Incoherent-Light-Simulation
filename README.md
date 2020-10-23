# Incoherent-Light-Simulation


This simulator works computing the field created by point sources with random phases and randomly placed inside a circle. 

Time averaging is done using Monte Carlo integration. 

Then, the simulation is represented and animated with matplotlib.

Check the [youtube video](https://www.youtube.com/watch?v=ySte6NRuA-k&list=PLYkZehxPE_IhJDMTJUob1ZbxWhL8AjHDi&index=1
) and the [article](https://rafael-fuente.github.io/visual-explanation-of-the-van-cittert-zernike-theorem-the-double-slit-experiment-with-incoherent-and-coherent-light.html) for further explanation:


## Installation

Just clone or download this repo.
The package requeriments are:

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


Also take a look at the [simulations of the double slit experiment with incoherent and coherent light](/double_slit_simulations)


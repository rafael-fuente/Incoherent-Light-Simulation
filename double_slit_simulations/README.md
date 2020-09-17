# Double Slit Simulations with Coherent and Incoherent Light

These are finite-difference time-domain(FDTD) simulations of the double slit experiment with coherent light, incoherent light and partially coherent light.

The simulations are performed at three different time scales: femtoseconds, picoseconds and microseconds to show the differences between them.

The simulations use the [open source FDTD meep simulator](https://meep.readthedocs.io/en/latest/)

The simulation is stored in [HDF5](https://www.h5py.org/) file format which is very good to store large amounts of data.
Then, the simulation is represented and animated with matplotlib.


## Installation

Just clone or download this repo.

The package requeriments are:

1. meep
2. numpy
3. h5py
4. matplotlib

To install meep follow the guide of the official page: https://meep.readthedocs.io/en/latest/Installation/

## Simulations

To perform the simulations, just run from the command prompt the corresponding Python scripts:

```
python simulation_coherent_femtoseconds.py
```

![animation](/double_slit_simulations/images/gaussian_femtoseconds.gif)


```
python simulation_coherent_picoseconds.py
```

![animation](/double_slit_simulations/images/gaussian_picoseconds.gif)


```
python simulation_incoherent_femtoseconds.py
```

![animation](/double_slit_simulations/images/incoherent_femtoseconds.gif)


```
python simulation_incoherent_picoseconds.py
```

![animation](/double_slit_simulations/images/incoherent_picoseconds.gif)

```
python simulation_partially_incoherent_femtoseconds.py
```

![animation](/double_slit_simulations/images/partially_coherent_femtoseconds.gif)


```
python simulation_partially_incoherent_picoseconds.py
```

![animation](/double_slit_simulations/images/partially_coherent_picoseconds.gif)




# Double Slit Simulations with Coherent and Incoherent Light

These are finite-difference time-domain (FDTD) simulations of the double slit experiment with coherent light, incoherent light and partially coherent light.

The simulations are performed at three different time scales: femtoseconds, picoseconds and microseconds to show the differences between them.

The simulations use the [open source FDTD meep simulator](https://meep.readthedocs.io/en/latest/)

The simulations are stored in [HDF5](https://www.h5py.org/) file format which is very good to store large amounts of data.
Then, the simulation are represented and animated with matplotlib.


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

[![animation](/double_slit_simulations/images/gaussian_femtoseconds.gif)](/double_slit_simulations/simulation_coherent_femtoseconds.py)


```
python simulation_coherent_picoseconds.py
```

[![animation](/double_slit_simulations/images/gaussian_picoseconds.gif)](/double_slit_simulations/simulation_coherent_picoseconds.py)


```
python simulation_incoherent_femtoseconds.py
```

[![animation](/double_slit_simulations/images/incoherent_femtoseconds.gif)](/double_slit_simulations/simulation_incoherent_femtoseconds.py)


```
python simulation_incoherent_picoseconds.py
```

[![animation](/double_slit_simulations/images/incoherent_picoseconds.gif)](/double_slit_simulations/simulation_incoherent_picoseconds.py)

```
python simulation_partially_incoherent_femtoseconds.py
```

[![animation](/double_slit_simulations/images/partially_coherent_femtoseconds.gif)](/double_slit_simulations/simulation_partially_incoherent_femtoseconds.py)


```
python simulation_partially_incoherent_picoseconds.py
```

[![animation](/double_slit_simulations/images/partially_coherent_picoseconds.gif)](/double_slit_simulations/simulation_partially_incoherent_picoseconds.py)



For the microseconds simulations, you need to run the simulation at least with 10000 samples and averaging them to get a denoised image. This task could take several hours in a personal computer. The smartest approach is taking a sample each time interval equal to the coherence time of the source: λ * λ / (c * Δλ). This is because it is the minimum time to make the electric field change considerably.
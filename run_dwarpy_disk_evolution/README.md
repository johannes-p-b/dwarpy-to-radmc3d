# Simulate a disk that evolves over time

Introduction
------------
This example directory is related to Carolin Kimmig's Dwarpy code.

Kimmig et al. "Dwarpy: A One-Dimensional Evolution Code for Warped Astrophysical Disks". JOURNAL (YEAR) ...

Dwarpy is used to simulate warped disks and their evolution in time. With RADMC-3D corresponding radiative transfer computations can quickly be performed. In the following, a radiative transfer simulation of a single Dwarpy disk is explained.

If you do not have Dwarpy installed yet, you can still perform a test simulation. This example directory contains the data of a warped disk created with Dwarpy. If you want to create your own disk, see the section below for a quick start with Dwarpy.

Note: To perform a simulation of single disks (i.e. no time evolution), visit the directory /single-disk-simulation.


Files
-----
This directory should contain the following files:

  README                         (This file)  
  Makefile                       (Only for convenient cleanmodel and cleanall)  
  dustkappa_silicate.inp         (some dust opacity file)  
  problem_setup.py               (a python script for setting up some input files)    
  problem_plotexamples.py        (a python script for imaging a disk)  
  dwarpy_data/warped_disk_evolution.rad	 (a folder containing a file with information on the disk at each point in the simulated time)  
  images/                        (a folder to save the images later)


Create your own evolving disk with Dwarpy
-----------------------------------------
The following lines give an example for a quick start with Dwarpy.

First, make sure you have Dwarpy installed: *LINK_TO_DWARPY*

Import the package to your python project.

  from dwarpy import *  
  from dwarpy.surfacedensity import * 

Then, create a disk object, for example a warped disk.

  disk_warped = WarpedDisk()

Specify where the disk data of the time evolution should be stored. The file that will contian the data must be a .pkl file.

  path_to_simulation_data = './simulation-data/warped_disk_test.pkl'

In order to start the simulation, call the following function.

  start_simulation(
      disk = disk_warped,
      file = path_to_simulation_data,
      dt = 0.1,
      n_steps = 1000,
      n_interm = 100,
      equations = dwarpy.simulation.GeneralizedRotReset,
  )

The data can be further proceeded by calling:

  warped_disk_evolution = SimulationResult(path_to_simulation_data)


Run this model
--------------
  1) Make sure you have compiled the main radmc3d code in src/ already.
     See manual for how to compile. 
  2) Type 
        python problem_setup.py
  3) In the shell type 'radmc3d mctherm' and wait until this is finished
     NOTE: Do not, as in run_simple_userdef_1/, type './radmc3d mctherm' (i.e.
     do not use the ./). NOTE: If you compiled the code with openmp,
     then you can speed up the code with e.g. 'radmc3d mctherm setthreads 4'.
  4) Make sure that the Python support libraries are installed. See the
     RADMC-3D manual for details on how to install the radmc3dPy and the
     radmc3d_tools libraries.  
  5) TBD  


29.03.2023

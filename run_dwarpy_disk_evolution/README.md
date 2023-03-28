# Disk evolution simulation

Introduction
------------



Note: For the simulation of single disks (i.e. no time evolution) see [Single disk simulation](#single-disk-simulation).
(Note: For the simulation of disks evolving in time see [Disk evolution simulation](#disk-evolution-simulation).)


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

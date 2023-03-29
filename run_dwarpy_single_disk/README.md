# Simulate a single disk

Introduction
------------
This directory is related to Carolin Kimmig's Dwarpy code: 

Kimmig et al. "Dwarpy: A One-Dimensional Evolution Code for Warped Astrophysical Disks". JOURNAL (YEAR) ...

Dwarpy is used to simulate warped disks and their evolution in time. With RADMC-3D corresponding radiative transfer computations can quickly be performed. In the following, a radiative transfer simulation of a single Dwarpy disk is explained.

If you do not have Dwarpy installed yet, you can still perform a test simulation. This example directory contains the data of a warped disk created with Dwarpy. If you want to create your own disk, see the section below for a quick start with Dwarpy.

Note: To do a simulation of a disk evolving in time, please visit the directory run_dwarpy_disk_evolution.

Files
-----
This directory should contain the following files:

  README                         (This file)  
  Makefile                       (Only for convenient cleanmodel and cleanall)  
  dustkappa_silicate.inp         (some dust opacity file)  
  problem_setup.py               (a python script for setting up some input files)    
  problem_plotexamples.py        (a python script for imaging the disk)  
  dwarpy_data/warped_disk.rad    (a folder containing a file with information on the disk, created with Dwarpy)
  
  
Create your own disk with Dwarpy
--------------------------------
Make sure you have installed Dwarpy: *LINK_TO_DWARPY*

Import the Dwarpy package to your Python project.

  from Dwarpy import * 

Then, create a disk object. For example, create a warped disk.

  warped_disk = WarpedDisk()

Then export it as a .rad file in the dwarpy_data directory and give the file a name.

  path_to_radmc3d = '..\radmc3d-2.0\examples\run_dwarpy_single_disk\dwarpy_data\warped_disk.rad'
  warped_disk.to_radmc3d(path_to_radmc3d)

For more detailed information please refer to the Dwarpy documentation.


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
  5a) Type 
        python problem_plotexamples.py

or

  5b) Go into python with matplotlib interactive mode:
        ipython --matplotlib
     Now you can use the problem_plotexamples.py to make an image and
     create some plots. Please read the problem_plotexamples.py script
     to learn how to do these things interactively. You can run this
     script from the python prompt with:
        %run problem_plotexamples.py




20.03.2023, 28.03.2023

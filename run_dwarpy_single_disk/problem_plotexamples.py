#
# Import packages
#
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from radmc3dPy.image import *
from radmc3dPy.analyze import *
from radmc3dPy.natconst import *


#
# Make sure to have done the following beforhand:
#
#  First compile RADMC-3D
#  Then run:
#   python problem_setup.py
#   radmc3d mctherm
#


#
# Make and plot image of disk at 1.65 microns: scatterd light
#
makeImage(npix=301, incl=0., phi=180., wav=1.65, sizeau=200., setthreads=8, nostar=True)  # this calls RADMC-3D
im_scat = readImage()

plt.figure()
plot_image = plotImage(im_scat, au=True, log=True, vmax=-12,vmin=-15, bunit='inu',cmap='hot')
#plt.savefig('disk_scattered_light.png', dpi=200)
plot_image['implot'].write_png('disk_scattered_light.png')
plt.show()


#
# Make and plot image of disk at 1.3 mm: thermal dust emission
#
"""
makeImage(npix=301, incl=0., phi=180., wav=1.3e3, sizeau=200., setthreads=8, nostar=True)  # this calls RADMC-3D
im_therm = readImage()


plt.figure()
plotImage(im_therm, au=True, log=True, maxlog=3, bunit='jy/pixel', dpc=130., cmap='magma')
plt.show()
"""

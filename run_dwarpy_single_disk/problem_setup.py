#
# Import packages
#
import numpy as np         # array handling
import pickle as pkl       # loading .rad files


#
# Some natural constants
#
au  = 1.49598e13     # Astronomical Unit       [cm]
pc  = 3.08572e18     # Parsec                  [cm]
ms  = 1.98892e33     # Solar mass              [g]
ts  = 5.78e3         # Solar temperature       [K]
ls  = 3.8525e33      # Solar luminosity        [erg/s]
rs  = 6.96e10        # Solar radius            [cm]
ss  = 5.6703e-5      # Stefan-Boltzmann const  [erg/cm^2/K^4/s]
GG  = 6.67408e-08    # Gravitational constant  [cm^3/g/s^2]
mp  = 1.6726e-24     # Mass of proton          [g]
kk  = 1.3807e-16     # Boltzmann's constant     [erg/K]


#
# Disk warping:
# Coordinate transformation to rotate (theta,phi) --> (theta',phi'),
# for a normal vector as a function of radius l(r) = (l_x,l_y,l_z),
# where the normal vector is in the cartesian coordinate system.
# A flat disk with midplane at the theta=pi/2 location is given by
# l(r) = (0,0,1).
#
# TODO: CHECK CREDITS IN RADMC-3D EXAMPLE FILE
def get_angle(x,y,positive=False):
    if np.isscalar(x):
        xx   = np.array([x])
        yy   = np.array([y])
    else:
        xx   = np.array(x)
        yy   = np.array(y)
    xx  += 1e-90*np.pi
    ang  = np.arctan(yy/xx)
    ang[xx<0] -= np.pi
    if positive:
        ang[ang<0] += 2*np.pi
    else:
        ang[ang<=-np.pi] += 2*np.pi
    if len(ang)==1:
        ang = ang[0]
    return ang

# Simple rotation counterclockwise
def rotate(x,y,ang):
    cos = np.cos(ang)
    sin = np.sin(ang)
    xp  = cos*x - sin*y
    yp  = sin*x + cos*y
    return xp,yp

def warped_coordinate_transformation(theta_3d,phi_3d,r_1d,lunit_1d):
    assert theta_3d.shape[0]==len(r_1d), 'Error in coordinate transformation: nr of elements of r_1d array does not match.'
    assert len(lunit_1d.shape)==2, 'Error in coordinate transformation: l_1d array must have [nr,3] elements.'
    assert lunit_1d.shape[0]==len(r_1d), 'Error in coordinate transformation: nr of elements of l_1d array does not match.'
    assert lunit_1d.shape[1]==3, 'Error in coordinate transformation: l_1d array must have [nr,3] elements.'
    theta_prime_3d = np.zeros_like(theta_3d)
    phi_prime_3d   = np.zeros_like(phi_3d)
    for ir in range(len(r_1d)):
        l     = lunit_1d[ir,:]
        ll    = np.sqrt(l[0]**2+l[1]**2+l[2]**2)
        l     = l/ll
        if l[0]==0 and l[1]==0:
            theta_prime_3d[ir,:,:] = theta_3d[ir,:,:].copy()
            phi_prime_3d[ir,:,:]   = phi_3d[ir,:,:].copy()
        else:
            angh  = get_angle(l[0],l[1])
            incl  = get_angle(l[2],np.sqrt(l[0]**2+l[1]**2))
            r     = r_1d[ir]
            theta = theta_3d[ir,:,:]
            phi   = phi_3d[ir,:,:]
            x     = r*np.sin(theta)*np.cos(phi)
            y     = r*np.sin(theta)*np.sin(phi)
            z     = r*np.cos(theta)
            xt,yt = rotate(x,y,-angh)
            xi,zi = rotate(xt,z,incl)
            xn,yn = rotate(xi,yt,angh)
            zn    = zi
            #rr    = np.sqrt(xn**2+yn**2+zn**2)
            pp    = get_angle(xn,yn,positive=True)
            tt    = get_angle(zn,np.sqrt(xn**2+yn**2))
            theta_prime_3d[ir,:,:] = tt
            phi_prime_3d[ir,:,:]   = pp
    return theta_prime_3d,phi_prime_3d


#
# Open disk data
#

# Path to disk data computed with the code Dwarpy (Kimmig et al., in prep.).
path = 'dwarpy_data/warped_disk.rad'

# This file contains information on the radial location of cell edges (corresponding to 'ri' in the 
# /run_ppdisk_analytic_1/problem_setup.py file), the radial cell centers ('rc'), the stellar mass 
# ('m_star'), the pressure scale height ('hp'), the dimensionless pressure scale height / aspect 
# ratio ('hpr'), the time (important if temporal disk evolution is studied in Dwarpy), the radial 
# surface density distribution of dust ('sigmad') and the l vectors for every disk annulus (l is 
# the normal vector of the annulus, respectively).
# TODO: CHECK DIMENSIONLESS PRESSURE SCALE HEIGHT

# Open .rad file and save data as a dictionary
with open(path, 'rb') as f:
    disk_data = pkl.load(f)


#
# Star paramters
#

#The stellar mass is the only relevant variable for Dwarpy. The remaining variables
# needed for the stellar luminosity calculation have to be specified here.
mstar = disk_data['m_star']
rstar = 1.54 * rs               # stellar radius
tstar = 7850.                   # stellar surface temperature
pstar = np.array([0.,0.,0.])    # standard location of the star in Dwarpy


#
# Grid setup
#

ri = disk_data['ri']
rc = disk_data['rc']

# Azimuthal and polar grids are not represented by Dwarpy and have to be specified 
# by the user.
ntheta   = 100
nphi     = 180
thetaup  = 0.2

thetai   = np.linspace(thetaup,np.pi-thetaup,ntheta+1)
thetac   = 0.5 * ( thetai[:-1] + thetai[1:] )

phii     = np.linspace(0.e0,np.pi*2.e0,nphi+1)
phic     = 0.5 * ( phii[:-1] + phii[1:] )

nr = len(rc)
ntheta = len(thetac)
nphi = len(phic)

# 3D grid
qq       = np.meshgrid(rc,thetac,phic,indexing='ij')
rr       = qq[0]
tt0      = qq[1]
pp0      = qq[2]


#
# Make warp
#

l = disk_data['l']
tt,pp = warped_coordinate_transformation(tt0,pp0,rc,l)
zr = np.pi/2.-tt


#
# Define cell's surface density, scale height and aspect ratio
#

# Dwarpy generated arrays (single axis - radial dependence only)
sigmad = disk_data['sigmad']   # surface density
hh = disk_data['hh']           # scale height
hhr = disk_data['hhr']         # aspect ratio (equal to hh / rc)

# We want 3D arrays with shape (nr,ntheta,nphi).
# Do pre-allocation
sigmad3d = np.zeros(rr.shape)
hh3d = np.zeros(rr.shape)
hhr3d = np.zeros(rr.shape)

# Fill arrays
for i in range(nr):
    sigmad3d[i] = np.tile(sigmad[i],ntheta*nphi).reshape(ntheta,nphi)
for i in range(nr):
    hh3d[i] = np.tile(hh[i],ntheta*nphi).reshape(ntheta,nphi)
for i in range(nr):
    hhr3d[i] = np.tile(hhr[i],ntheta*nphi).reshape(ntheta,nphi)


#
# Make 3D density array, corresponding to the grid defined previously
#
rhod = (sigmad3d / (np.sqrt(2.e0*np.pi)*hh3d)) * np.exp(-(zr**2/hhr3d**2)/2.e0)


#
# Write the wavelength_micron.inp file
#
lam1     = 0.1e0
lam2     = 7.0e0
lam3     = 25.e0
lam4     = 1.0e4
n12      = 20
n23      = 100
n34      = 30
lam12    = np.logspace(np.log10(lam1),np.log10(lam2),n12,endpoint=False)
lam23    = np.logspace(np.log10(lam2),np.log10(lam3),n23,endpoint=False)
lam34    = np.logspace(np.log10(lam3),np.log10(lam4),n34,endpoint=True)
lam      = np.concatenate([lam12,lam23,lam34])
nlam     = lam.size
with open('wavelength_micron.inp','w+') as f:
    f.write('%d\n'%(nlam))
    for value in lam:
        f.write('%13.6e\n'%(value))
#
# Write the stars.inp file
#
with open('stars.inp','w+') as f:
    f.write('2\n')
    f.write('1 %d\n\n'%(nlam))
    f.write('%13.6e %13.6e %13.6e %13.6e %13.6e\n\n'%(rstar,mstar,pstar[0],pstar[1],pstar[2]))
    for value in lam:
        f.write('%13.6e\n'%(value))
    f.write('\n%13.6e\n'%(-tstar))
#
# Write the amr_grid.inp file
#
with open('amr_grid.inp','w+') as f:
    f.write('1\n')                       # iformat
    f.write('0\n')                       # AMR grid style  (0=regular grid, no AMR)
    f.write('100\n')                     # Coordinate system: spherical
    f.write('0\n')                       # gridinfo
    f.write('1 1 1\n')                   # Include r,theta coordinates
    f.write('%d %d %d\n'%(nr,ntheta,nphi))  # Size of grid
    for value in ri:
        f.write('%13.6e\n'%(value))      # X coordinates (cell walls)
    for value in thetai:
        f.write('%13.6e\n'%(value))      # Y coordinates (cell walls)
    for value in phii:
        f.write('%13.6e\n'%(value))      # Z coordinates (cell walls)
#
# Write the dust density file
#
with open('dust_density.inp','w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n'%(nr*ntheta*nphi))     # Nr of cells
    f.write('1\n')                       # Nr of dust species
    data = rhod.ravel(order='F')         # Create a 1-D view, fortran-style indexing
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
#
# Write the dustopac.inp file
#
with open('dustopac.inp','w+') as f:
    f.write('2               Format number of this file\n')
    f.write('1               Nr of dust species\n')
    f.write('============================================================================\n')
    f.write('1               Way in which this dust species is read\n')
    f.write('0               0=Thermal grain\n')
    f.write('silicate        Extension of name of dustkappa_***.inp file\n')
    f.write('----------------------------------------------------------------------------\n')


#
# Write the radmc3d.inp file
#
nphot_therm = 100_000
nphot_scat = 500_000
with open('radmc3d.inp','w+') as f:
    f.write(f'nphot = {nphot_therm}\n')
    f.write(f'nphot_scat = {nphot_scat}\n')
    f.write('scattering_mode_max = 1\n') # isotropic scattering
    f.write('iranfreqmode = 1\n')
    f.write('mc_scat_maxtauabs = 5.d0')



# TODO: Function for refining Dwarpy radial cells


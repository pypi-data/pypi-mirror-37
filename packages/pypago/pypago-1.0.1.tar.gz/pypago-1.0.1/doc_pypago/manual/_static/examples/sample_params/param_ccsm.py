
"""
This program contains the main settings of |pypago|.

This is the only file that the user is likely to modify.
"""

import numpy as np
import pylab as plt
import matplotlib as mp
from mpl_toolkits.basemap import pyproj
import sys

ee = pyproj.Geod(ellps='GRS80')  # ellipsoid used for distance calculation

rho0_c = 4.186e6  # for heat transport calculations
S0 = 34.8  # reference salinity for freshwater calculations

# Sigma vectors (used in density related transport indices)
sigma0_vec_lr = np.array([24, 24.4, 24.9, 25.4, 25.9, 26.4,
                        26.75, 27.05, 27.30, 27.45, 27.58, 27.68, 27.75,
                        27.80, 27.83, 27.86, 27.89, 27.92, 27.95, 27.98,
                        28.01, 28.04, 28.07, 28.1, 28.6, 29.1])
sigma0_vec_hr = np.array([24, 24.2, 24.4, 24.65, 24.9, 25.15, 25.4, 25.65,
                        25.9, 16.15, 26.4, 16.57, 26.75, 26.90, 27.05, 27.17,
                        27.30, 27.37, 27.45, 27.52, 27.58,
                        27.63, 27.68, 27.72, 27.75, 27.78, 27.80, 27.815,
                        27.83, 27.845, 27.86, 27.875, 27.89,
                        27.905, 27.92, 27.935, 27.95, 27.965,
                        27.98, 27.99, 28.01, 28.025,
                        28.04, 28.055, 28.07, 28.085, 28.1, 28.35,
                        28.6, 28.8, 29.1])
sigma2_vec = np.array([34.4, 34.6, 34.8, 35, 35.2, 35.4, 36, 36.4,
                       36.6, 36.7, 36.8, 36.9, 36.95, 37, 37.05,
                       37.1, 37.15, 37.2, 37.4, 37.6, 38])
sigma1_vec = np.arange(29.68, 34.6800+1, 1)

lev1 = 500  # first depth interval from surface down to lev1
lev2 = 1000  # second depth interval from lev1 down to lev2
lev3 = 2000  # third depth interval from lev2 m down to lev3 m

# settings for the figures
mp.rcParams['lines.linewidth'] = 1.  # line width
mp.rcParams['text.usetex'] = False  # no latex in matplotlib

left = 0.07
right = 0.99
wspace = 0.07
top = 0.93
bottom = 0.03
figsize = (11, 4)
bgcolor = 'black'
cmapt = plt.cm.get_cmap('jet')
cmaps = plt.cm.get_cmap('jet')
cmapv = plt.cm.get_cmap('RdBu_r')

# Uncomment below to change the output
#sys.stdout = open('log.txt', 'w')
#sys.stderr = sys.stdout
file_stdout = sys.stdout
file_stderr = sys.stderr

# List of coordinate variable names
dictvname = {}
dictvname["lon_varname"] = "TLONG"
dictvname["lat_varname"] = "TLAT"
dictvname["bathy_varname"] = "HT"
dictvname["tmask_varname"] = "REGION_MASK"

dictvname["dxt_varname"] = "DXT"
dictvname["dyt_varname"] = "DYT"
dictvname["dye_varname"] = "HTE"
dictvname["dxn_varname"] = "HTN"
dictvname["dzt_varname"] = "dz" 

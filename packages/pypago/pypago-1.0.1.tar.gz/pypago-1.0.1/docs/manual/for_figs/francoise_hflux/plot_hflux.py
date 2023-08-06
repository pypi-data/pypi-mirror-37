# -*- coding: utf-8 -*-

"""
Script that reproduces the figure of the paper by Barrier. et al (2014)

.. todo:: handle error (file not found)

.. todo:: link to builddoc for instruction to get input files

.. todo:: input files outside of working space
"""

from __future__ import print_function

import sys
from mpl_toolkits.basemap import Basemap, shiftgrid
import pylab as plt
from netCDF4 import Dataset
from netcdftime import utime
import numpy as np
import pypago.pyio
import pypago.misc
import pypago.sections
from matplotlib.patches import Polygon

# Reading of the netcdf file
try:
    filein = Dataset('./hflux_1m_194801_201212_NCEP.nc', 'r')
except RuntimeError:
    print('no ./hflux_1m_194801_201212_NCEP.nc')
    sys.exit(-1)

lon = filein.variables['lon'][:]
lat = filein.variables['lat'][:]
hflux = filein.variables['hflux'][:]
time = filein.variables['time']
units = time.units
time = time[:]
cdftime = utime(units)

# Extraction of the dates, conversion in format YYYYMM (year month)
date = [cdftime.num2date(time_temp) for time_temp in time]
yyyy = np.array([d.year*100+d.month for d in date])
year = yyyy/100
month = yyyy - 100*year

# Computation of the anomalies
anom = np.empty(hflux.shape)
for mmm in np.unique(month):
    itemp = np.nonzero(month == mmm)[0]
    clim = np.tile(np.mean(hflux[itemp, :, :], axis=0), (len(itemp), 1, 1))
    anom[itemp, :, :] = hflux[itemp, :, :] - clim

# computation of the standard deviation, and grid shift
anom_std = np.std(anom, axis=0)
anom_std, lon = shiftgrid(180, anom_std, lon, start=False)

dsox = [-34, -22]
dsoy = [68., 65.5]
ifox = [-15., -7.5]
ifoy = [65., 62.5]
fsox = [-7.5, -5.]
fsoy = [62.5, 58.]
mdnx = [-3, 7]
mdny = [57, 60]
nonx = [-22., -0.5,15.]
nony = [77.5, 77.,78.]
barx = [18, 15]
bary = [69, 78]
marx = [-21.065,  -34.685, -35.459]
mary = [64.86,    56.189, 53.036]
qdex = [-35.459,   -9.]
qdey = [53.036,   52.]
qdwx = [-35.459,  -53.]
qdwy = [53.036, 47.]
bafx = [-64, -52]
bafy = [66, 67]
hudx = [-65, -66]
hudy = [59, 64]
itsx = [-6, -4]
itsy = [55, 57]
spux = [-56.355, -56.2]
spuy = [52.406, 51.223]
ovix = [-44.2000,  -30.7000, -12.2000, -7.5000]
oviy = [60.1000,  58.7000, 40.3000, 40.2800]
arsx = [-56, -47]
arsy = [53, 61.500]
avcx = [-42.5000,  -7.5]
avcy = [61.5000,  40.2800]

sections_list = []
sections_list.append(pypago.sections.Section('mar', marx, mary, len(marx)*['NE']))
sections_list.append(pypago.sections.Section('42e', qdex, qdey, len(qdex)*['NE']))
sections_list.append(pypago.sections.Section('fso', fsox, fsoy, len(fsox)*['NE']))
sections_list.append(pypago.sections.Section('42w', qdwx, qdwy, len(qdwx)*['NE']))
sections_list.append(pypago.sections.Section('dso', dsox, dsoy, len(dsox)*['NE']))
sections_list.append(pypago.sections.Section('baf', bafx, bafy, len(bafx)*['NE']))
sections_list.append(pypago.sections.Section('hud', hudx, hudy, len(hudx)*['NE']))


# ================================= Plotting
plt.figure()
ax = plt.gca()

# Drawing of the map background
m = Basemap(llcrnrlon=-80, llcrnrlat=30, urcrnrlon=20, urcrnrlat=80, resolution='l')
m.drawcoastlines(linewidth=0.5, zorder=11)
m.fillcontinents(zorder=10)

# Drawing of the eastern Polygon
xpoly = []
ypoly = []
for secnames in ['mar', '42e', 'fso']:
    section = sections_list[pypago.misc.findsecnum(sections_list, secnames)]
    if secnames == 'fso':
        section.lon = section.lon[::-1]
        section.lat = section.lat[::-1]
    xpoly = xpoly + list(section.lon)
    ypoly = ypoly + list(section.lat)
xpoly = np.array(xpoly)
ypoly = np.array(ypoly)
xy = np.transpose(np.array([xpoly, ypoly]))
pol = Polygon(xy, closed=True, fill=False, hatch='/')
ax.add_artist(pol)

# Drawing of the western Polygon
xpoly = []
ypoly = []
for secnames in ['mar', 'dso', 'baf', 'hud', '42w']:
    section = sections_list[pypago.misc.findsecnum(sections_list, secnames)]
    if secnames in ['toto']:
        section.lon = section.lon[::-1]
        section.lat = section.lat[::-1]
    xpoly = xpoly + list(section.lon)[::-1]
    ypoly = ypoly + list(section.lat)[::-1]
xpoly = np.array(xpoly)
ypoly = np.array(ypoly)
xy = np.transpose(np.array([xpoly, ypoly]))
pol = Polygon(xy, closed=True, fill=False, hatch='\\')
ax.add_artist(pol)

# Contouring
lon, lat = np.meshgrid(lon, lat)
cs = m.contourf(lon, lat, anom_std, levels=np.arange(20, 160, 20),
                extend='both', cmap=plt.cm.YlOrRd)
colorbar = m.colorbar(cs, location='bottom')
colorbar.set_label('Monthly winter heat flux anomalies Std ($W.m^{-2}$)')

# ++ save only in not called by sphinx
plt.savefig('figure.png', bbox_inches='tight')

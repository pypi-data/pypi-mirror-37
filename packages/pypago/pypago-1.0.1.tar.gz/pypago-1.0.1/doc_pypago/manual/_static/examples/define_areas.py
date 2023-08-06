import pypago.areas
import pypago.pyio
import pylab as plt
import numpy as np

# load the grid and grid sections
grid = pypago.pyio.load('data/natl_grid.pygo')

# define a polygone and extract the i,j indexes of the points within the domain
lonpol = [-60, -41, -28, -44]
latpol = [62, 48, 65, 60]
i, j = pypago.areas.extract_dom_from_pol(grid, lonpol, latpol)

# create the area object
areaname = 'areatest'
areas = pypago.areas.Areas(grid, areaname, i, j)

# Plot the domain area

plt.figure()
plt.subplot(2, 1, 1)
plt.title('Bathymetry (geographical coordinates)')
grid.bathy = np.ma.masked_where(grid.mask==0, grid.bathy)
plt.pcolor(grid.lont, grid.latt, grid.bathy)
plt.plot(lonpol, latpol)

plt.subplot(2, 1, 2)
plt.title('Area mask (index coordinate)')
grid.plot_mask()
plt.imshow(areas.mask, origin='lower', interpolation='none')
plt.savefig('figs/domdef_pol.png', bbox_inches='tight')

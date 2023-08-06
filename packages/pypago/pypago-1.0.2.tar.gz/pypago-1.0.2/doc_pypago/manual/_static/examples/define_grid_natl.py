
"""
Extraction of a sub-domain grid. Three examples
are provided: natl grid, North-Atlantic Grid
or natl ocean (with a longitude flip).
"""

import pylab as plt
import pypago.grid

# natl example
jmin = 80
jmax = None
imin = 90
imax = 160

coord = pypago.pyio.load('data/nemo_coords.pygo')

# if you do not have a coord object saved in a file, use:
# coord = pypago.coords.create_coord("NEMO", 'data/mesh_mask.nc')

# creation grid
grid = pypago.grid.create_grid(coord,
                               jmin=jmin, jmax=jmax, 
                               imin=imin, imax=imax)

# saving of the grid
pypago.pyio.save(grid, 'data/natl_grid.pygo')

# drawing the domain on top of the
# coord mask
plt.figure()
coord.plot_mask()
grid.plot_dom()
plt.title('global domain')
plt.savefig('figs/natl_domain')

# drawing the domain mask
plt.figure()
grid.plot_mask()
plt.title('natl grid')
plt.savefig('figs/natl_grid')

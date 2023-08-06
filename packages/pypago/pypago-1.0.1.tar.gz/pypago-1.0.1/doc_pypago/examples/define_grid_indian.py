
"""
Extraction of a sub-domain grid. Three examples
are provided: indian grid, North-Atlantic Grid
or Indian ocean (with a longitude flip).
"""

import pylab as plt
import pypago.grid

# indian example
jmin = 10
jmax = 100
imin = 140
imax = 40

coord = pypago.pyio.load('data/nemo_coords.pygo')

# if you do not have a coord object saved in a file, use:
# coord = pypago.coords.create_coord("NEMO", 'data/mesh_mask.nc')

# creation grid
grid = pypago.grid.create_grid(coord,
                               jmin=jmin, jmax=jmax, 
                               imin=imin, imax=imax)

# saving of the grid
pypago.pyio.save(grid, 'data/indian_grid.pygo')

# drawing the domain on top of the
# coord mask
plt.figure()
coord.plot_mask()
grid.plot_dom()
plt.title('global domain')
plt.savefig('figs/indian_domain')

# drawing the domain mask
plt.figure()
grid.plot_mask()
plt.title('indian grid')
plt.savefig('figs/indian_grid')

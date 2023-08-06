
"""
Extraction of a sub-domain grid. Three examples
are provided: Global grid, North-Atlantic Grid
or Indian ocean (with a longitude flip).
"""

import pylab as plt
import pypago.grid

coord = pypago.pyio.load('data/nemo_coords.pygo')
# if you do not have a coord object saved in a file, use:
# coord = pypago.coords.create_coord("NEMO", 'data/mesh_mask.nc')

# creation grid
grid = pypago.grid.create_grid(coord)

# saving of the grid
pypago.pyio.save(grid, 'data/global_grid.pygo')

# drawing the domain on top of the
# coord mask
plt.figure()
coord.plot_mask()
grid.plot_dom()
plt.title('global domain')
plt.savefig('figs/global_domain')

# drawing the domain mask
plt.figure()
grid.plot_mask()
plt.title('global grid')
plt.savefig('figs/global_grid')

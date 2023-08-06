
"""
Extraction of model coordinates,
and saving into a Pygo file.
"""

import pypago.coords

modelname = 'NEMO'
filename = 'data/mesh_mask.nc'

# loading coords
coord = pypago.coords.create_coord(modelname, filename)

pypago.pyio.save(coord, 'data/nemo_coords.pygo')

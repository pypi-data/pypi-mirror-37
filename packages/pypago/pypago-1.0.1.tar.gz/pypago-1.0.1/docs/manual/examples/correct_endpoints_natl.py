
"""
Correction of North-Atlantic section endpoints
and saving into a new file.
"""

import pypago.pyio
import pypago.sections

dirin = '/Users/Nicolas/Documents/data/PAGO/pago_neworca/'
example = 'natl'
sect = pypago.pyio.load('%s/pygo/endpoints/%s_section_endpoints.pygo' %(dirin, example))
grid = pypago.pyio.load('%s/pygo/grid/%s_grid.pygo' %(dirin, example))

secname = 'hud'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire = ['SE']

secname = 'baf'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire = ['SW']

secname = '42n'
index = pypago.misc.findsecnum(sect, secname)
sect[index].lat[-1] = 53

secname = 'ifo'
index = pypago.misc.findsecnum(sect, secname)
sect[index].lat[-1] = 62

secname = 'fso'
index = pypago.misc.findsecnum(sect, secname)
sect[index].lat[0] = 62

secname = 'nos'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire[-1] = 'NW'

secname = 'non'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire[0] = 'NW'

pypago.pyio.save(sect, '%s/pygo/endpoints/%s_corr_section_endpoints.pygo' %(dirin, example))

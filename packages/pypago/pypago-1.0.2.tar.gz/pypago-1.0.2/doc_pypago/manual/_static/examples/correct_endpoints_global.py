
"""
Correction of Global section endpoints
and saving into a new file.
"""

import pypago.pyio
import pypago.sections

dirin = '/Users/Nicolas/Documents/data/PAGO/pago_neworca/'
example = 'global'
sect = pypago.pyio.load('%s/pygo/endpoints/%s_section_endpoints.pygo' %(dirin, example))

secname = 'ITF'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire = ['SW']

secname = 'DSO'
index = pypago.misc.findsecnum(sect, secname)
sect[index].lat[-1] -= 1

secname = 'P4N'
index = pypago.misc.findsecnum(sect, secname)
sect[index].dire = ['NW']

pypago.pyio.save(sect, '%s/pygo/endpoints/%s_corr_section_endpoints.pygo' %(dirin, example))

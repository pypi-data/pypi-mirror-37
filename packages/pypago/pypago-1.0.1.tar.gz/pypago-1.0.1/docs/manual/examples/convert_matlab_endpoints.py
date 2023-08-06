
"""
Example of conversion of Matlab's section endpoints
into PyPago section endpoints
"""

from subprocess import call
import pypago.mat
import pypago.pyio

dirin = '/Users/Nicolas/Documents/data/PAGO/pago_neworca/'

filename = '%s/matlab/sections_GL.mat' %dirin
gl_sec = pypago.mat.secmat_topygo(filename)

filename = '%s/matlab/sections_NA.mat' %dirin
na_sec = pypago.mat.secmat_topygo(filename)

call(['mv', '%s/matlab/sections_NA.pygo' %dirin,
      '%s/pygo/endpoints/natl_section_endpoints.pygo' %dirin])

call(['mv', '%s/matlab/sections_GL.pygo' %dirin,
      '%s/pygo/endpoints/global_section_endpoints.pygo' %dirin])

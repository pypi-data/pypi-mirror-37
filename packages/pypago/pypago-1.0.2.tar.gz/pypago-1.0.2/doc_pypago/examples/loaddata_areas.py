import pypago.pyio
import pypago.data

modelareas = pypago.pyio.load('data/natl_domain.pygo')

filenameT = 'data/dyna_grid_T.nc'

dirvarT = {'temp':'votemper', 'salt': 'vosaline', 
           'hf':'sohefldo', 'ssh':'sossheig'}

modelareas = pypago.data.loaddata_area_t(modelareas, filenameT, dirvarT)

modelareas = pypago.data.loadtime(modelareas, filenameT)

pypago.pyio.save(modelareas, 'data/natl_datadom.pygo')

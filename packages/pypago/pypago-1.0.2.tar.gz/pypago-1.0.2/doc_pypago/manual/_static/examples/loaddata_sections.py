import pypago.pyio
import pypago.data

modelsec = pypago.pyio.load('data/indian_gridsec.pygo')

filenameT = 'data/dyna_grid_T.nc'
filenameU = 'data/dyna_grid_U.nc'
filenameV = 'data/dyna_grid_V.nc'

# loading data on T points
dirvarT = {'temp':'votemper', 'salt': 'vosaline'}
modelsec = pypago.data.loaddata_sec_u(modelsec, filenameT, dirvarT)

# loading data on U/V points
dirvarUV = {'vel':['vozocrtx', 'vomecrty']}
modelsec = pypago.data.loaddata_sec_uv(modelsec, filenameU, filenameV, dirvarUV)

# loading time array
modelsec = pypago.data.loadtime(modelsec, filenameT)

pypago.pyio.save(modelsec, 'data/indian_datasec.pygo')

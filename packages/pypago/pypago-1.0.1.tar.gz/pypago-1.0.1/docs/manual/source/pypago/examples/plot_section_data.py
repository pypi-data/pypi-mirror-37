import pypago.pyio
import pypago.plot
import pypago.misc
import pylab as plt
import numpy as np

# change the section colors without going into the code
from cycler import cycler
plt.rcParams['axes.prop_cycle'] = cycler(color=['cyan', 'magenta', 'gold', 'orange'])

# loading of the gridded section domain
sections = pypago.pyio.load('data/natl_datasec.pygo')

idsec = pypago.misc.findsecnum(sections, 'section2')
sec = sections[idsec]

# conversion of velocity into cm/s
sec.vel *= 100

plt.figure(figsize=(14, 8))
# draw temperature as pcolorplot
cs, cb = pypago.plot.pcolplot(sec, 'temp', istracer=1)
# add colorbar label
cb.set_label('Temperature (C)')
# modify colorbar limit
cs.set_clim(0, 14)
# draw temperature as contourplot
cl = pypago.plot.contourplot(sec, 'temp', istracer=1, levels=np.arange(0, 20, 2), colors='k')
# add label
plt.clabel(cl)
# add grid
plt.grid(True)
plt.savefig('figs/section_temp.png', bbox_inches='tight')

plt.figure(figsize=(14, 8))
# draw salinity as pcolorplot
cs, cb = pypago.plot.pcolplot(sec, 'salt', istracer=1)
# add colorbar label
cb.set_label('Salinity (psu)')
# modify colorbar limit
cs.set_clim(34, 36)
# draw salinity as contourplot
cl = pypago.plot.contourplot(sec, 'salt', istracer=1, levels=np.arange(34, 36.5, 0.25), colors='k')
# add label
plt.clabel(cl)
# add grid
plt.grid(True)
plt.savefig('figs/section_salt.png', bbox_inches='tight')

plt.figure(figsize=(14, 8))
# draw velocity as pcolorplot
cs, cb = pypago.plot.pcolplot(sec, 'vel', istracer=0)
# add colorbar label
cb.set_label('velocity (cm/s)')
# modify colorbar limit
#cs.set_clim(-5, 5)
# draw velocity as contourplot
cl = pypago.plot.contourplot(sec, 'vel', istracer=1, levels=np.arange(-6, 7, 2), colors='k')
# add label
plt.clabel(cl)
# add grid
plt.grid(True)
plt.savefig('figs/section_vel.png', bbox_inches='tight')

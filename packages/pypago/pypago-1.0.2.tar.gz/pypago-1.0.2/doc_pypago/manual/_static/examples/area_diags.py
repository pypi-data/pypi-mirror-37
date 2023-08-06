import pypago.pyio
import pypago.misc
import pypago.secdiag as secdiag
import pypago.areadiag as areadiag
import pylab as plt
import numpy as np
from pypago.sample_param import rho0_c

data = pypago.pyio.load('data/natl_datadom.pygo')
area = data[0]

# calculation of the SSH * SSH product within the area
# and adding it to the area structure
area.surfhc = area.temp[:, 0, :] * area.ssh

# calculation of domain heat content
hc = areadiag.volume_content(area, 'temp')

# calculation of surface integral of SST * SSH
surfhc = areadiag.surface_content(area, 'surfhc')

# adding the surface heat content to the total heat content
hc += surfhc

# calculation of surface heat flux
hf = areadiag.surface_content(area, 'hf')

# loading of the gridded section domain
sections = pypago.pyio.load('data/natl_datasec.pygo')

# computation of heat convergence
heatconv = areadiag.compute_tracer_conv(area, sections, 'temp', 'vel')

# Conversion of hc and heat conv into J and W, respectively
hc *= rho0_c   # J
heatconv *= rho0_c    # W 

# calculation of dt and conversion into seconds
dt = area.time[1:] - area.time[0:-1]
dt = np.array([d.total_seconds() for d in dt])

# time derivative of ocean heat content
dhc = np.diff(hc) / dt

# averaging of heat convergence and heat flux 
# to fit the location of hc
heatconv = 0.5*(heatconv[1:] + heatconv[:-1])
hf = 0.5*(hf[1:] + hf[:-1])

# conversion from W into PW
hf *= 1e-15
dhc *= 1e-15
heatconv *= 1e-15

# Plotting
plt.figure()
ax1 = plt.gca()
plt.plot(dhc, label=r'$\partial hc  / \partial t$')
plt.plot(hf, label='$H_{flux}$')
plt.plot(heatconv + hf, label='$H_{flux} + H_{conv}$')
plt.legend(loc=8)
ax1.set_ylabel('(PW)')
ax2 = ax1.twinx()
plt.plot(heatconv, label='$H_{conv}$', color='plum')
plt.xlim(0, len(hf)-1)
ax2.set_ylabel(r'$H_{conv}$' + ' (PW)', color='plum')
plt.setp(ax2.get_yticklabels(), color='plum')
plt.savefig('figs/heat_budget.png')

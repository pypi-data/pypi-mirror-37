import pypago.pyio
import pypago.misc
import pypago.secdiag as diag
import pylab as plt
import numpy as np
from pypago.sample_param import rho0_c

# loading section data
sections = pypago.pyio.load('data/indian_datasec.pygo')

# extraction of the "section4" section
indsec = pypago.misc.findsecnum(sections, 'section4')
sec = sections[indsec]

# creation of xticklabels
index = np.arange(0, len(sec.time))
xlabels = np.array([d.strftime('%Y-%m-%d') for d in sec.time])

# calculation of net volume transport
netvt = diag.net_volume_trans(sec, velname='vel') * 1e-6

# calculation of net heat transport
netht = diag.net_tracer_trans(sec, 'temp', velname='vel') * 1e-15 * rho0_c

# calculation of velocity without net transport
current_nonet = diag.remove_spatial_mean(sec, 'vel')

# calculation of total heat transport (i.e. without net mass transport)
totht = diag.total_tracer_trans(sec, 'temp', 'vel') * 1e-15 * rho0_c

# calculation of temperature anomalies
temp_nonet = diag.remove_spatial_mean(sec, 'temp')

# overturning volume transport
ovvt = diag.overturning_volume_transport(sec, 'vel')

# overturning heat transport
ovht = diag.overturning_tracer_transport(sec, 'temp', 'vel') * 1e-15 * rho0_c

# barotropic volume transport
barvt = diag.barotropic_volume_transport(sec, 'vel')

# barotropic heat transport
barht = diag.barotropic_tracer_transport(sec, 'temp', 'vel') * 1e-15 * rho0_c

# baroclinic heat transport
bcht = diag.baroclinic_tracer_transport(sec, 'temp', 'vel') * 1e-15 * rho0_c

plt.figure()
plt.subplots_adjust(left=0.1, right=0.99, 
                    top=0.95, bottom=0.05, hspace=0.25)

plt.subplot(2, 2, 1)
plt.plot(totht, label='totht')
plt.plot(ovht + barht + bcht, label='sum')
plt.title('totht')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(ovht)
plt.title('ovht')

plt.subplot(2, 2, 3)
plt.plot(barht)
plt.title('barht')

plt.subplot(2, 2, 4)
plt.plot(bcht)
plt.title('bcht')

plt.savefig('figs/heat_transport.png')

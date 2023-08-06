import pypago.sections
import pypago.pyio
import pylab as plt

grid = pypago.pyio.load('data/natl_grid.pygo')

sect = pypago.pyio.load('data/endpoints_natl.pygo')

gridsec, badsec = pypago.sections.extract_grid_sections(grid, sect)

pypago.pyio.save(gridsec, 'data/natl_gridsec.pygo')

plt.figure()
grid.plot_mask()
for s in gridsec:
    s.plotsecfaces()
plt.savefig('figs/natl_gridsec.png')

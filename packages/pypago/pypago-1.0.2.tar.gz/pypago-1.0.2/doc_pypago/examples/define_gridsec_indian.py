import pypago.sections
import pypago.pyio
import pylab as plt

grid = pypago.pyio.load('data/indian_grid.pygo')

sect = pypago.pyio.load('data/endpoints_indian.pygo')

gridsec, badsec = pypago.sections.extract_grid_sections(grid, sect)

pypago.pyio.save(gridsec, 'data/indian_gridsec.pygo')

plt.figure()
grid.plot_mask()
for s in gridsec:
    s.plotsecfaces()
plt.savefig('figs/indian_gridsec.png')

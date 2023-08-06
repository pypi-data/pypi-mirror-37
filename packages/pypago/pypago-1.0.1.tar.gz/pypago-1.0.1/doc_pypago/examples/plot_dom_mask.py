import pypago.pyio
import pypago.plot
import pylab as plt

# change the section colors without going into the code
from cycler import cycler
plt.rcParams['axes.prop_cycle'] = cycler(color=['cyan', 'magenta', 'gold', 'orange'])

grid = pypago.pyio.load('data/natl_grid.pygo')

data = pypago.pyio.load('data/natl_datadom.pygo')
mask = data[0].mask

# loading of the gridded section domain
sections = pypago.pyio.load('data/natl_datasec.pygo')

plt.figure(figsize=(8,6))
plt.subplots_adjust(top=0.95, bottom=0.05, hspace=0.3, 
                    left=0.05, right=0.95)

plt.subplot(2, 2, 1)
pypago.plot.plot_dom_mask(grid, None, None)
plt.title('Grid mask')

plt.subplot(2, 2, 2)
pypago.plot.plot_dom_mask(grid, sections, None)
plt.title('Grid mask + sections')

plt.subplot(2, 2, 3)
pypago.plot.plot_dom_mask(grid, None, mask)
plt.title('Grid mask + domain mask')

plt.subplot(2, 2, 4)
pypago.plot.plot_dom_mask(grid, sections, mask)
plt.title('Grid mask + sections + domain mask')

plt.savefig('figs/plot_dom_mask.png', bbox_inches='tight')

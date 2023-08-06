====
Grid
====

Gridded ocean data often come in a global scale, while regional investigations
only need part of the grid.
In order to lighten the memory requirements, in PAGO function
:func:`sections_MODEL`, a subset of the grid is defined (using variables lonw,
lone, lats and latn as grid indices of the corners of the subset) and used to
load all data.
If the analysis is carried in the North Atlantic, the program proposes limits
for the grid subset, appropriate for the default sections.
Indeed, section end-points and corners must locate within the limits of the
grid subset.
The user can also manually define the limits of the grid subset.
Once the grid subset is defined, all grid and data information is cropped over
the region of interest.
Because of interpolation of tracers from the center of the grid cells to the
faces, the grid subset is limited in latitude (1 < lats,latn < nlat), and we
assume periodicity in longitude when needed.
The latter is also assumed when lonw > lone, which is allowed by the program
(see figure below).

The grid subset can be saved into :file:`.mat` file and used again when
defining new sections.

.. figure:: _static/fig10.jpg
   :alt: alternate fig10.jpg
   :width: 90%

.. TODO
.. ====
..
.. produce figure.
.. caption
..
.. EVOLUTIONS
.. ==========
..
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/grid.html

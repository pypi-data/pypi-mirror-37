=====
Areas
=====

The current version of programs only allows to diagnose tracer budget within
the North Atlantic subpolar gyre and the Nordic Seas.
Further developments will extend this possibility to other regions.
The definition of areas, in PAGO function :func:`sections_MODEL`, must be
compatible with sections: the whole perimeter of the area is either made of
continental coasts or sections.
This actually depends on the spatial resolution of the dataset.
For example, the Strait of Belle Isle, that separates the island of
Newfoundland from the Labrador Peninsula, is usually closed in climate models
but may be open in high resolution datasets.
Besides, the positive direction defined for each section closing the area must
be considered carefully when defining the convergent transports in PAGO
function :func:`volumes_MODEL`.
Data information within areas, i.e. temperature, salinity and volume (to keep
track of volume changes as in z* models like GFDL-CM3) is loaded by PAGO
function loaddata_*.
Volume indices, calculated by PAGO function :func:`volumes_MODEL`, are time
series that describe heat, salt and freshwater (defined using a reference
salinity of 34.8, to be modified in :func:`volumes_MODEL` directly) budgets:

- tracer content within the whole area (from surface to bottom),
- tracer content within fixed vertical intervals.
  The limits of those intervals, defined in :func:`volumes_MODEL`, is fixed but
  their actual depth depends on the depth of the data levels as there is no
  vertical interpolation of the data.
- advective convergence to the area, from surface to bottom and for fixed
  vertical intervals.

.. EVOLUTIONS
.. ==========
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/areas.html

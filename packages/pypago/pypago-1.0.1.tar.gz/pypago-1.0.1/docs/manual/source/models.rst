.. _models:

======
Models
======

.. index:: CMIP5

The package is currently delivered for analysis of 4 climate models:

- GFDL-CM3 (Griffies et al., J. Clim., 2011),
- NCAR-CCSM4 (Gent et al., J. Clim, 2011),
- CNRM-CM5 (Voldoire et al., Clim. Dyn., 2012) and
- IPSL-CM5 (Dufresne et al., Clim. Dyn., 2012).

We assume that variable names of data and grid characteristics are those of
IPCC CMIP5 simulations.

Cf. `CMIP5 Data Reference Syntax (DRS) and Controlled Vocabularies <http://cmip-pcmdi.llnl.gov/cmip5/docs/cmip5_data_reference_syntax.pdf>`_
for files, directories, metadata, and URLs to identify CMIP5 datasets.

.. todo:: add this publication to biblio


GFDL-CM3 has vertical levels of variable thickness, which we take into account
by analyzing transports rather than velocities.
Those transports are available at the center of the grid faces, hence no
interpolation of the velocities is required (although GFDL is a B-grid model).
NCAR-CCSM4 has a parameterization of the overflow across Denmark Strait, which
prescribes velocities at few grid points at the bottom.
We do not make special treatment for this parameterization.
Interpolation of the velocities is made as follows.
The volume transport at the corner of the grid cells is computed and then split
in 2 to the center of each adjacent faces.
Using this method, we do not make any assumption on the lateral conditions
(free slip or no slip) and ensure that the volume transport is exactly
conserved.
Characteristics regarding the grid must be contained in a single file.
They must include: the length of the grid faces, the size of the grid cell at
its center, the longitude and latitude of the grid points,
the land / ocean mask, the bathymetry and the thickness of the vertical
levels (at the center of the grid cell and at the center of the faces in case
partial steps are implemented).
Other models may be analyzed using the package, by simply adapting the variable
names of data and grid characteristics.

HYDROBASE climatology can also be analyzed using the package - more details
will come soon.

.. todo:: hydrobase still in roadmap ?

..
.. EVOLUTIONS
.. ==========
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/models.html

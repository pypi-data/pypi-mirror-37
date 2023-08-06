.. _output:

======
Output
======

|pago| uses |matlab| structures to store information regarding grid and
outputs, which can be directly saved in :file:`.mat` files:

- MODEL_grid contains the limits of the subset of the grid that is analyzed,
  longitude, latitude and mask over this subset,
- MODEL_sections contains all information for each section: grid
  characteristics, section indices and data along the section,
- MODEL_area contains all information for each area: grid characteristics,
  area indices and data within area,
- MODEL_indices contains information about the transport across each section,
- MODEL_volumes contains information about the volume content and convergence
  for each area.

|pago| functions :func:`loaddata_*` and :func:`indices_MODEL` use a so-called
structfile as argument.
This :file:`.mat` file contains variables MODEL_grid, MODEL_sections and
eventually MODEL_area.
This file is originally produced by PAGO function :func:`sections_MODEL`, with
NaN values instead of data output at the first time step.
Data variables are then concatenated with actual data output by loaddata_*.
PAGO also offers the possibility to save the information in |netcdf| format.

- data along sections (:func:`create_netcdf_sec`) ie temperature, salinity and
  normal velocity, as well as some grid information: length, depth and area of
  each cell.
  This file is suitable for visual browsers of |netcdf| files such as ncview.
- indices describing the transport across sections (:func:`create_netcdf_ind`),
  over 30 time series.
  See comments of the |netcdf| file and description of index calculation for
  full description of the time series.
- indices describing the volume content and convergence
  (:func:`create_netcdf_vol`), nearly 30 time series.
  See comments of the |netcdf| file and description of volume calculation for
  full description of the time series.

When the package is used to diagnose monthly data, the user may want to
calculate yearly averages of the time series.
Depending on the convention used to produce the data, each month may or may not
have the same number of days.
|pago| offers a possibility to compute yearly averages of monthly indices,
taking into account leap years, 360-day-years and 365-day-years (yrave_volumes,
yrave_indices).

.. EVOLUTIONS
.. ==========
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/output.html

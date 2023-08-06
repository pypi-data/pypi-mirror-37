========
Overview
========

Inter-comparison of model and gridded observations of the ocean is a challenge
when they use different grids.
Interpolation from one grid to another brings eventual errors that may affect
significantly large scale budgets of tracers (heat, salt, freshwater).
This suite of programs offers the possibility to analyze gridded ocean data
along physical sections with minimum interpolation.
For example, this allows to monitor the circulation across an observed array
in various model outputs, whatever their spatial resolution or type of
discretization (B- or C- grids).
When defining sections that enclose a specific volume, large scale budgets of
tracers can be reconstruct and inter-compared among all kinds of gridded ocean
data.

The core of |pago| programs consists of finding the suite of west and north
grid faces to go from one geographical landmark to another, following the
geodesic distance.
Temperature and salinity are averaged from the centers of the 2 adjacent grid
cells to the center of the grid faces (taking into account missing values in
land).
Velocities, if available, are either located at the center of the grid faces
(in case of C-grids), or at the corners (B-grids).
In case of C-grid data, no interpolation is required for the velocities.
In case of B-grid data, the volume transport at the corner of the grid cells
is computed and then split in 2 to the center of each adjacent faces (see more
details in the :ref:`models` page).

.. plot:: ../for_figs/francoise_hflux/plot_hflux.py
   :include-source: false
   :nofigs:

.. _fig_striking_figure:

.. only:: html

   .. figure:: ../for_figs/francoise_hflux/figure.png
      :alt: ../for_figs/francoise_hflux/figure.png

      Location of sections and areas used by Barrier et al. 2015
      ([Barrier2015]_) to diagnose heat budget of the North Atlantic subpolar
      gyre.
      The latter is enclosed to the north by the Greenland-Scotland Ridge and
      Davis Strait, along which sections are defined to diagnose all incoming
      fluxes from higher latitudes.
      The choice of definition of the southern boundary of the subpolar gyre is
      more disputable as it is widely open to lower latitudes ; here it follows
      the geographical constraint imposed by Reykjanes Ridge in splitting the
      subpolar gyre in two subregions (identified by the hatchings).
      Color shading represents variability in the winter air-sea heat fluxes ;
      the latter is maximum in the western subpolar gyre, and its structure is
      well captured by one of the two subregions.
      As discussed in Barrier et al. 2015 ([Barrier2015]_), those two
      subregions of the subpolar
      gyre are significantly different in their dynamical responses to
      variability in the atmosphere and in adjacent oceanic regions.
      As a result, diagnosing volume, heat and freshwater budgets in the two
      subregions of the North Atlantic subpolar gyre separately is crucial and
      only possible with the flexibility of |pago| in the definition of
      sections and areas for ocean model diagnostics.

.. only:: latex

   .. figure:: ../for_figs/francoise_hflux/figure.png
      :alt: ../for_figs/francoise_hflux/figure.png

      Location of sections and areas used by Barrier et al. 2015 to diagnose
      heat budget of the North Atlantic subpolar gyre.
      The latter is enclosed to the north by the Greenland-Scotland Ridge and
      Davis Strait, along which sections are defined to diagnose all incoming
      fluxes from higher latitudes.
      The choice of definition of the southern boundary of the subpolar gyre is
      more disputable as it is widely open to lower latitudes ; here it follows
      the geographical constraint imposed by Reykjanes Ridge in splitting the
      subpolar gyre in two subregions (identified by the hatchings).
      Color shading represents variability in the winter air-sea heat fluxes ;
      the latter is maximum in the western subpolar gyre, and its structure is
      well captured by one of the two subregions.
      As discussed in Barrier et al. 2015, those two subregions of the subpolar
      gyre are significantly different in their dynamical responses to
      variability in the atmosphere and in adjacent oceanic regions.
      As a result, diagnosing volume, heat and freshwater budgets in the two
      subregions of the North Atlantic subpolar gyre separately is crucial and
      only possible with the flexibility of |pago| in the definition of
      sections and areas for ocean model diagnostics.

.. only:: latex

   .. todo:: citation reference Barrier et al. 2015 in latexpdf output

Here is the list of the main PAGO functions to be called:

- :func:`sections_MODEL` reads data regarding grid characteristics only,
  selects the region of interest when uploading the data, and identifies
  sections and areas on which circulation, and tracer content will be
  diagnosed.

- loaddata_* uploads the data output and extracts the information required
  along preselected sections and areas.
  This function also interpolates velocity and tracer data at the center of
  west and north grid faces, when needed.

- :func:`indices_MODEL` calculates simple or full diagnostics of the
  circulation (transport of volume, heat, salt and freshwater) across selected
  sections at each time step.

- :func:`volumes_MODEL` calculates thermal, haline and freshwater content
  within selected areas at each time step.
  It also calculates advective convergence of tracers at the boundaries or
  areas.

In order to make it easier for a new user to become familiar with this suite
of functions, there are few ready-to-use |matlab| scripts that contain the full
list of steps from the definition of the sections to the indices and the
mapping of the diagnostics (:file:`script_PAGO_*`).

The development of this package is still ongoing.
Please inform us of any bugs or necessary improvements.

.. TODO
.. ====
..
.. rst link
..
.. matlab vs python
..
..
.. liens matlab et pypago
..
.. improve biblio citation
..
.. Barrier2015 reference in PDF not ok : need fix
..
.. EVOLUTIONS
.. ==========
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/index.html
..
.. - fplod 20150608T142714Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * update reference paper citation
..
.. - fplod 20150703T160328Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * use bibtex file :file:`pago.bib` with sphinx extension
..
.. - fplod 20150914T085629Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * give up usage of sphinxcontrib-bibtex
..
.. - fplod 20150914T134955Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * add striking figure and associated legend and biblio reference
..
.. - fplod 20150914T165120Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * replace hard coded figure file of striking figure by execution of
..     plot_hflux.py
..
.. - fplod 20150915T142138Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * workaround of citation usage issue in caption for latexpdf output
..
.. - fplod 20151104T101435Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * externalize "howtocite"
..   * evolution chronological order because at the end of this file

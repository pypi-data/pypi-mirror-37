.. _mapago_requirements:

============
Requirements
============

|matlab|
========

The package has been developed for |matlab| R2012a, but it also works for
previous versions of |matlab|.

In this document, links point on the current last |matlab| release
documentations.

During interactive |matlab| session, :func:`help` and :func:`doc` functions
provide informations on the current running |matlab|.

.. todo:: test with later releases

   cf. http://fr.mathworks.com/help/matlab/release-notes.html?searchHighlight=release%20notes

.. warning:: Huge Postscript and PDF files

   .. todo:: find an official declaration instead of the following CR
      statement

   The last releases of |matlab| (R2014 and R2015) contain a bug that
   makes vector figures (`eps` and `pdf` format) unusable in scientific
   publications. Figures are either
   rasterized or too large to be used (>20 Mb).

It requires :

- the Mapping toolbox for use of 
  
  - function :func:`distance` (`distance` <http://fr.mathworks.com/help/map/ref/distance.html>`_)
  - function :func:`almanac` (`almanac` <http://fr.mathworks.com/help/map/ref/almanac.html>`_)
  - function :func:`axesm` (`axesm` <http://fr.mathworks.com/help/map/ref/axesm.html>`_)
  - function :func:`pcolorm` (`pcolorm` <http://fr.mathworks.com/help/map/ref/pcolorm.html>`_)
  - function :func:`plotm` (`plotm` <http://fr.mathworks.com/help/map/ref/plotm.html>`_)

.. todo::

   follow |matlab| advice : 

   almanac is not recommended. 
   Use earthRadius, referenceEllipsoid, referenceSphere, or wgs84Ellipsoid instead.

- the Statistics and Machine Learning Toolbox for use of functions

  - :func:`nanmax` (`nanmax <http://fr.mathworks.com/help/stats/nanmax.html>`_)
  - :func:`nansum` (`nansum <http://fr.mathworks.com/help/stats/nansum.html>`_)
  - :func:`nanmean` (`nanmean <http://fr.mathworks.com/help/stats/nanmean.html>`_).

Data are read in |netcdf| format, using |mapago| function :func:`readnc`.
This function is written for the built-in |matlab| R2012 |netcdf|
`functions <http://fr.mathworks.com/help/matlab/network-common-data-form.html>`_.
For older versions of |matlab| that do not have those built-in functions,
user may consider using :func:`readnc-old` (changing its name into
:func:`readnc`) that allows the use of the CSIRO netcdf-matlab interface and
|matlab| |netcdf| toolbox.

.. todo:: readnc-old.m not in repository

   fix the solution for readnc if |matlab| version < R2012

Similarly, user may have to use :func:`create_netcdf_*_old` functions instead
of the regular ones.

Data may be accessed remotely on OPeNDAP servers, using |mapago|
function :func:`readdap` instead of :func:`readnc`.

See the example of GFDL model analysis.

.. todo:: provide example

.. EVOLUTIONS
.. ==========
..
.. - fplod 20150929T111213Z guest-242.locean-ipsl.upmc.fr (Darwin)
..
..   * doc8
..   * add warning about huge image files
..   * official toolboxes names
..   * add links on the current matlab official release
..
.. - fplod 20150529T155953Z callisto.locean-ipsl.upmc.fr (Linux)
..
..   * hand made migration from html to rst from
..     http://www.whoi.edu/science/PO/pago/requirements.html

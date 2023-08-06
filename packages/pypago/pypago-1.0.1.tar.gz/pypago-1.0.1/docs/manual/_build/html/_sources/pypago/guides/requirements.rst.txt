.. _pypago_requirements:

============
Requirements
============

.. index:: Python 2.7

Prior to using |pypago|, the user must install Python and the libraries
that are listed in :numref:`t_lib`. These packages can be installed
by using package managers (:command:`Synaptic`, :command:`apt`,
:command:`macport`, :command:`fink`).

.. _t_lib:

.. list-table:: List of the Python libraries used in |pypago|
   :header-rows: 1

   * - Library
     - Website
   * - :py:mod:`numpy`
     - http://www.numpy.org/
   * - :py:mod:`matplotlib`
     - http://matplotlib.org/
   * - :py:mod:`netCDF4`
     - https://github.com/Unidata/netcdf4-python/
   * - :py:mod:`mpl_toolkits.basemap`
     - http://matplotlib.org/basemap/

New Python users are invited to use the `Anaconda Scientific
Python
distribution <https://www.continuum.io/downloads/>`_,
which automatically installs Python and the most used libraries,
among which :py:mod:`numpy`, :py:mod:`matplotlib` and :py:mod:`netCDF4`. The
:py:mod:`mpl_toolkits.basemap`  library, which is not included
in the default Anaconda distribution, can be
installed by using the :command:`conda` command as follows:

.. code-block:: bash

   conda install basemap

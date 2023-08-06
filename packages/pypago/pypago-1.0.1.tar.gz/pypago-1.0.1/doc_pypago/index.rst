.. PyPAGO documentation master file, created by
   sphinx-quickstart on Fri Nov 17 17:03:40 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/pago_background.jpg
   :width: 100%
   :align: center

|


Welcome to PyPAGO's documentation!
==================================

This document describes the Python version of the "Physical Analysis
of Gridded Ocean" (|pypago| hereafter) set of |matlab| programs available at
http://www.whoi.edu/science/PO/pago/.
This set of programs aims at comparing multiple fields (such as temperature, salinity and
velocity) of gridded ocean models along pre-defined sections.

The main difference between the Python and |matlab| versions are:

- Graphical User Interface (GUI) that has been developed, in order to make
  it more user-friendly (see :numref:`endpoints_gui` and :numref:`gridsec_gui`)
- An easy way to define closed domains from gridded sections (see :numref:`closedom_sec`), hence allowing the computation of closed budgets (heat budgets for instance, see :numref:`budgets_calc`)
  )
- The possibility to extract as many variables as you want, for instance, biogeochemical variables (see :numref:`loaddata`)

If you find a bug or want to contribute, please contact us at `pago-dev@groupes.renater.fr`_

.. _pago-dev@groupes.renater.fr: pago-dev@groupes.renater.fr

 .. toctree::
   :maxdepth: 2
   :caption: Contents:
   :numbered:

   intro
   manual
   api
   biblio

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

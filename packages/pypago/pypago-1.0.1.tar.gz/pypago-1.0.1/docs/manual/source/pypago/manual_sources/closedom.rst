
Definition of domains
#############################

|pago| allows to define closed domains, in which budgets calculations can be performed.
This is down by using the :py:class:`pypago.areas.Area` class.


Defining a domain using polygons
*********************************

The user can define a closed polygon by using a longitude/latitude polygon 
by using the :py:func:`pypago.areas.extract_dom_from_pol` function.

This function takes as argument the :py:class:`pypago.grid.Grid` class associated with
the model, the longitude and the latitude of the polygon. 

.. literalinclude::
    ../examples/define_areas.py

.. ipython:: python

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/define_areas.py"
        with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python

    print(areas)

.. _fig_domdef_pol:

.. figure:: ../examples/figs/domdef_pol.png
   :align: center
   
   Definition of a triangular domain from a polygon

.. note::
    If the polygon is not closed, it is closed automatically by the program

.. todo::
    Extend to circular domains?


.. _closedom_sec:

Defining a domain using gridded sections
****************************************

Another possibility for defining closed domains is to use gridded sections as boundaries. This is 
especially usefull when computing heat budgets and assessing the relative contributions
of surface heat fluxes and ocean heat advection (:cite:`Barrier2015`).

This is achieved by using the interactive script :py:class:`pypago.bin.make_areas` as follows:

.. literalinclude::
    ../examples/script_areas.sh

The arguments are the grid file, the gridded section file and the output file.

As a first step, the program displays
:numref:`fig_domdef1`. And in the terminal, the program
asks the names of the sections that close
the domain and their orientations ("in" if the transport is oriented
toward the domain, "out" if the transport is oriented out of the
domain). In the terminal, this gives:

.. parsed-literal::

    name of the area? natldom
    give names of the sections (separate the names by a space) section1 section2 section3 section4
    give orientation of the sections (in: directed toward the basin/out directed out of the area) in in in out

The program then generates a :file:`.png` file that contains
i) the land points in black
ii) the wet points in gray
iii) the initialisation of the domain mask in white.
This png file is displayed in :numref:`fig_domdef2`.

.. _fig_domdef1:

.. figure:: _static/figs/domdef_1.png
   :align: center

   First figure displayed by the program for the generation of
   closed domains.

.. _fig_domdef2:

.. figure:: _static/figs/mask_init_natldom.png
   :align: center
   :scale: 300 %

   :file:`PNG` file created by the :py:func:`pypago.pypago_grid.areas_MODEL`
   function (:file:`mask_init_natldom.png`).

Then, a message is prompted by the terminal:

.. parsed-literal::

    Edit the mask_init_spg.png file using gimp, paint 
    or any other software. Fill in white the area enclosed 
    in your boundaries. Save the new png file as mask_init_spg_bis.png.
    When done, press any key
    
To complete the creation of the domain, an image manipulation image
must be called in. In this step, the user must manually complete the
mask by filling in white the inside of the domain. The user must also
carefully check that no pixel has been missed. In our example, the
resulting :file:`.png` file is presented in :numref:`fig_domdef2`.
When the :kbd:`ENTER` key is pressed, the figure displayed on
:numref:`fig_domdef4` and the following message is displayed:

.. parsed-literal:: 

    Check that the domain mask is well defined 
    (i.e. between the section lines). If not, 
    reconsider the png edition
    Is it ok? (0 if not) 1

The user must check that the white area is well positioned in regards
with the section. 
If the domain is not well defined (for instance, a pixel is missing), 
the user is invited to re-edit the :file:`.png` file. If the user is ok with the domain, 
he is proposed to define another section. 

.. parsed-literal::

    Define another area? (0 or 1) 0

.. _fig_domdef3:

.. figure:: _static/figs/mask_init_natldom_bis.png
   :align: center
   :scale: 300 %

   PNG file created using Gimp :file:`mask_init_spg_natldom.png`.

.. _fig_domdef4:

.. figure:: _static/figs/domdef_2.png
   :align: center

   When the :kbd:`ENTER` key is pressed...

The output file contains the :py:class:`pypago.areas.Areas` class.

.. ipython:: python

    import pypago.pyio
    
    area = pypago.pyio.load('data/natl_domain.pygo')
    print(area[0])

Note that contrary to domains defined from polygons, domains defined from sections have 2 additional arguments:
- :samp:`secnames` is a list of the names of the sections that define the domain
- :samp:`signs` is a list of the signs of the section transport regarding to the domain budget (:samp:`+1` if the section transport is toward the domain, :samp:`-1` if the transport is outward of the domain).

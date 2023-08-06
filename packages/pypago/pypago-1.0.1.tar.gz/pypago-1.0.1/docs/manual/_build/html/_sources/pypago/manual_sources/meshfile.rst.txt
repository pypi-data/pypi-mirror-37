
Create gridded sections
##########################

Once the section longitude and latitude endpoints have been defined, and the :samp:`param.py` file has been
properly set, the next step is to process the model grid. This is achieved in three steps:

#.  Coordinates and scale factors are extracted over the entire domain and stored into a
    :py:class:`pypago.coords.Coords` object.
#.  Coordinates and scale factors are extracted over the region of interest, and 
    the variables are eventually zonally flipped. The subdomain variables are stored in a
    :py:class:`pypago.grid.Grid` object.
#.  Finally, the section endpoints are converted into the :py:class:`pypago.grid.Grid` object, and
    sections out of the domain are discarded.

These steps can be performed either by using Python scripts or by using the  
:py:mod:`pypago.guis.gui_grid_model` Python program. 

.. warning::

    These steps require a NetCDF file containing the variables defined in the :samp:`dictvname` variable (either default values or values defined in the :samp:`param.py` file).

Both methods are described bellow.

Using Python scripts
********************

Extracting coord objects
========================

Extraction of coord objects is achieved by using the :py:func:`pypago.coords.create_coord` function as follows:

.. literalinclude:: 
    ../examples/define_coords.py
 
.. ipython:: python

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/define_coords.py"
        with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python

    print(coord)

Note that the user may also use the executable program :py:mod:`pypago.bin.make_coords` as follows:

.. literalinclude:: 
    ../examples/script_coords.sh

The arguments are the model name, the path of the meshfile and the path of the output file.

.. note::
    The :samp:`param.py` file still needs to be in the working directory


Extracting grid objects
=======================

The grid objects are obtained by using the :py:func:`pypago.grid.create_grid` function.

Its arguments are the i (:samp:`imax` and :samp:`imin`) and j (:samp:`jmin` and :samp:`jmax`) indexes of the subdomain to extract. When one argument is :samp:`None`, then the higher (or lower) possible index is taken. Note that if :samp:`imax<imin`, zonal periodicity is assumed.

.. warning::
    
    For regional studies, :samp:`imax` should always be greater than :samp:`imin`

An example of a subdomain extraction with zonal periodicity is shown below.

.. literalinclude:: 
    ../examples/define_grid_indian.py
    
.. ipython:: python

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/define_grid_indian.py"
        with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python
    
    print(grid)

.. figure:: ../examples/figs/indian_domain.png
    :align: center
    
    Extracting the Indian Ocean from a global grid

.. figure:: ../examples/figs/indian_grid.png
    :align: center
    
    Indian domain that has been extracted
    
Note that the user may also use the executable program :py:mod:`pypago.bin.make_grid` as follows:

.. literalinclude:: 
    ../examples/script_grid.sh

This script is an interactive script which allows to chose the values of the 
:samp:`imin`, :samp:`imax`,  
:samp:`jmax` and :samp:`jmin` variables. The arguments are the model name, 
the model mesh file and the name of the output file.

Extracting gridded sections
===========================

The extraction of gridded section is achieved by using the :py:func:`pypago.sections.extract_grid_sections` function.

The function takes as arguments the :py:class:`pypago.grid.Grid` object and the list of section endpoints (:py:class:`pypago.sections.Section` objects).
It returns a list of :py:class:`pypago.sections.GridSection` objects (:samp:`gridsec` in the example below) and the indexes of the discarded sections (:samp:`badsec` in the example below). 

.. literalinclude:: 
    ../examples/define_gridsec_indian.py

.. ipython:: python

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/define_gridsec_indian.py"
        with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python

    print(badsec)
    for sec in gridsec:
        print(sec)

 
.. figure:: ../examples/figs/indian_gridsec.png
    :align: center
    
    Indian Ocean gridded sections


The user is strongly invited to use the executable program :py:mod:`pypago.bin.make_gridsec`, which is run as follows:

.. code-block:: bash

    make_gridsec.py grid.pygo endpoints.pygo gridsec.pygo

This interactive program allows the user to check that the sections are well defined (see **Warning** below), and gives the possibility to correct badly defined sections. It takes as argument the name of the name of the |pago| grid and endpoints file,  and the name of the output file.

.. warning:: 
    It is essential to verify that the orientations of the segments are 
    consistent, i.e. that the dots are on the same side of the line, as in 
    :numref:`fig_ihmgrid7`. If this is not the case, the section orientation must be corrected.

    Furthermore, to perform budgets within a basin, it is essential to ensure that the basin is closed (i.e. that
    there is no leakage). If not, it might be necessary to add another section or to displace points from sea to land.

.. _gridsec_gui:

Using graphical user interface
******************************

The extraction of gridded sections may also be achieved through the use of the
:py:mod:`pypago.guis.gui_grid_model` Python program. This opens the GUI
that is shown in :numref:`fig_ihmgrid1`.

.. _fig_ihmgrid1:

.. figure:: _static/figs/grid_1.png
   :scale: 40 %

   GUI of the :py:mod:`pypago.pypago_guis.gui_grid_model`  program

Menus
=====

The :py:mod:`pypago.pypago_guis.gui_grid_model` is made of a
:menuselection:`File` menu and
of a :menuselection:`Section` menu.
The :menuselection:`File` menu is made of a :menuselection:`Quit` item (quit
the application), an :menuselection:`Open` item and
:menuselection:`Save`/:menuselection:`Save As` items.
The :menuselection:`Open` item is used to load the model meshfile, containing
all the scale factors of the model configuration. It must be a |netcdf| file.
The :menuselection:`Save`/:menuselection:`Save As` items are used to save the
outputs of the |pypago| programs that convert the section endpoints into model
indices.

The :menuselection:`Section` menu only contains a
:guilabel:`Load section` item,
which is used to load section endpoints that have been generated by
the :py:mod:`pypago.pypago_guis.gui_sections_edition` program.
Note that is menu item is deactivated until a meshfile has been loaded.

Opening a meshfile
==================

As a first step, the user must define the name of the model that is
going to be processed. This is done by setting the :guilabel:`Model`
ComboBox. Then, the user must load the |netcdf| meshfile of the model by
using the :menuselection:`Open` menu item. When this is done, the
mask of the model is plotted, as shown in
:numref:`fig_ihmgrid2`, and the default domain is plotted as a black
rectangle. The next step is to edit the domain, for instance by
reducing the size of the domain according to the section positions.

.. _fig_ihmgrid2:

.. figure:: _static/figs/grid_2.png
   :scale: 40 %

   Example of the mask of a global model configuration (here,
   the CNRM model).

Domain edition
==============

The domain edition is handled by the top-left widgets. The
:guilabel:`min_i`, :guilabel:`max_i`, :guilabel:`min_j` and :guilabel:`max_j`
widgets control the domain left, right i-indices and bottom, top
j-indices, respectively. Default values are set to the biggest
possible domain.

The section can be changed by "click and drag" on the corner
points (but not on the lines) or by a change in the TextControl
widgets. In the latter case, the changes are validated when the :kbd:`ENTER`
key is pressed. Such a change is shown in :numref:`fig_ihmgrid3`.

With this specific grid, the user interested in the Indian Ocean might
be a little disappointed, since the box domain does not cross it. In
order to overcome this issue, the user must set, in the TextControl
widgets, a value for :guilabel:`min_i` that is greater than the value of
:guilabel:`min_j`. This switches the previous box into two boxes, as shown
in :numref:`fig_ihmgrid4`. With this layout, the user can define
a domain that encompasses the Indian Ocean.

.. _fig_ihmgrid3:

.. figure:: _static/figs/grid_3.png
   :scale: 40 %

   Example of a change in domain

.. _fig_ihmgrid4:

.. figure:: _static/figs/grid_4.png
   :scale: 40 %

   Example of a change in domain, when the min\_i value is
   greater than the min\_j value.

Loading a section file
======================

When the meshfile is loaded and the subdomain selected, the user must
now the section endpoints that have been generated using the
:py:mod:`pypago.pypago_guis.gui_sections_edition`.
When this is done, the program
computes the model indices that are associated with the section
endpoints (these indices are model dependent) and draw the sections as
"stairs", as shown in :numref:`fig_ihmgrid5`.
When this is done, the top-left RadioBox activates and switches to
:guilabel:`Check sections`.

.. _fig_ihmgrid5:

.. figure:: _static/figs/grid_5.png
   :scale: 40 %

   Section "stairs" that are drawn when loading a section file
   into the :py:mod:`pypago.pypago_guis.gui_grid_model` program.

Checking and editing the sections
=================================

When these "stairs" are plotted, the user must verify that they are
well defined. The points that appear on the figure and which define
the direction where the transport is counted positive must all be on
the same side of the line, as in :numref:`fig_ihmgrid7`. If it is
the case, the user can save the model indices that are associated with
the sections into a file, by using the
:menuselection:`Save`/:menuselection:`Save As` menu items.

If they are not, the user must change the direction of the bad
segments. This is done by switching the RadioBox to
:guilabel:`Edit Sections`. This edition mode is similar to the one
described previously, except that the section edition can only be
achieved by modifying the point positions.  Furthermore, if the user
plans to perform budgets within closed domains, he needs to check that
the sections indeed define a closed domain.

If the domain is too large compared to the section positions, the user
may also be interested in reducing the size of the domain. This is
done by switching the RadioBox to :guilabel:`Edit Sections`.
Note that the :menuselection:`Save`/:menuselection:`Save As` menu item is only
activated when this RadioBox is set to :guilabel:`Check Sections`, in order to
force the user to check that the sections are well defined.

.. _fig_ihmgrid7:

.. figure:: _static/figs/grid_7.png
   :scale: 40 %

   Gridded section


.. _fig_ihmgrid6:

.. figure:: _static/figs/grid_6.png
   :scale: 40 %

   Section correction

When the user is done, he can save the outputs of the program into 
:file:`.pygo` files. If the chosen saving path is :samp:`/output/path/file.pygo`,
the :samp:`Grid` object will be saved in the :samp:`/output/path/file_grid.pygo` file,
while the :samp:`GridSec` objects will be saved in the :samp:`/output/path/file_gridsec.pygo` file.

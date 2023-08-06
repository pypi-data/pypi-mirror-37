
Definition of section longitude/latitude endpoints
##################################################

One of the main purpose of |pypago| is to compute transport indices across pre-defined
sections. Therefore, the first step is to define the section longitude
and latitude endpoints. 

The user can either define section endpoints directly in a Python script, by using the
:py:class:`pypago.sections.Section` class, or by using an interactive GUIS.

Definition of endpoints in a file
*********************************

An example of section endpoits definition is provided below:

.. literalinclude:: 
    ../examples/define_endpoints.py

.. ipython:: python 

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/define_endpoints.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)
    
.. ipython:: python

    print(section)

First, the list of section endpoints (*listofsec* variable) is initialised as an empty list. Then, one section 
is created by using the :py:class:`pypago.sections.Section` class by providing the name, longitude, latitude and direction of the
segments.  Then, the section is added to the section list.

Then, the list of sections is saved by using the :py:func:`pypago.pyio.save` function.

.. warning::

    The user must **absolutely** save a list of section endpoints, even if only one section is defined.

.. _endpoints_gui:

Definition of endpoints using a GUI
************************************
    
This is achieved by running the
:py:mod:`pypago.guis.gui_sections_edition` program.
It opens the GUI that is shown in :numref:`fig_ihmsec1`.

Menus
=====

The program for the section edition is made of 2 menus, the
:menuselection:`File` menu and the :menuselection:`Background` menu.

The :menuselection:`File` menu is made of a :guilabel:`Quit` item (quit the
application), an :guilabel:`Open` item (opening of a section endpoints file)
and of :menuselection:`Save`/:menuselection:`Save As` items (save the section
endpoints into a file).

The :menuselection:`Background` menu is made of a single item, the
:guilabel:`Load Background` item, which allows to open a |netcdf| file and to
use it as a map background. This file must contain a two-dimensional
variable as well as the spatial coordinates associated with these
variables. The names of the spatial coordinates must match the names
of the file dimension. For instance, a :command:`ncdump` applied on the
file used below returns something like

.. parsed-literal::

   netcdf processed\_gebco_08_\-12_32_14_50 {
   dimensions:
           lat = 2160 ;
           lon = 3120 ;
   variables:
           float lat(lat) ;
           float lon(lon) ;
           float bathy(lat, lon) ;
   }

To use a background field defined on an irregular grid (for instance a NEMO model output), here are the steps to follow. Assume you have the following file:

.. parsed-literal::

   netcdf nemo\_mbathy {
   dimensions:
        t = UNLIMITED ; // (1 currently)
        y = 264 ;
        x = 567 ;            
    variables:
        short mbathy(t, y, x) ;
        float nav_lat(y, x) ;
        float nav_lon(y, x) ;
   }

You can  modify the file by using the following NCO commands:

.. code-block:: bash

    # rename the dimensions so that the names match the coordinates
    ncrename -O -d x,nav_lon -d y,nav_lat nemo_mbathy.nc nemo_mbathy.nc 
    
    # remove the spurious time dimension
    ncwa -O -a t nemo_mbathy.nc nemo_mbathy.nc

The file should now be:

.. parsed-literal::

    netcdf nemo_mbathy {
    dimensions:
        nav_lat = 264 ;
        nav_lon = 567 ;
    variables:
        short mbathy(nav_lat, nav_lon) ;
            mbathy:cell_methods = "t: mean" ;
        float nav_lat(nav_lat, nav_lon) ;
        float nav_lon(nav_lat, nav_lon) ;
    }


Map handling
============

In the upper-left corner, the widgets are intended to map handling:

#. The :guilabel:`lone`, :guilabel:`lonw`, :guilabel:`lats`, :guilabel:`latn`
   TextControl widgets allow to edit the geographical limits of the map
   (eastern and western longitudes, southern and northern latitudes
   respectively).
   The default setting displays a global map.
   To validate changes, the :kbd:`ENTER` key must be pressed in the
   TextControl widget.
#. The :guilabel:`lon0` and :guilabel:`boundinglat` TextControl widgets allow
   to edit the values of the central longitude and of the bounding latitude
   for the northern and southern pole-centered projections.
   To validate changes, the :kbd:`ENTER` key must be pressed in the
   TextControl widget.
#. The :guilabel:`projection` ComboBox allows to select the projection of the
   map.
   The available projections are Cylindrical Equidistant
   (:samp:`cyl`, default), North-Polar Stereographic (:samp:`npstere`),
   South-Polar Stereographic (:samp:`spstere`) and
   Lambert Conformal (:samp:`lcc`).
#. The :guilabel:`resolution` ComboBox allows to change the resolution
   of the map.
   The available resolutions are crude (:samp:`c`, default), low (:samp:`l`),
   intermediate (:samp:`i`), high (:samp:`h`) and full (:samp:`f`). The
   full resolution must only be used for very localised studies.
#. The :guilabel:`Plot mode` ComboBox allows to change the map
   background plot. When set to :samp:`Filled continents`, continents
   are filled in gray and coastlines are drawn in black. If set to
   :samp:`ETOPO`, the background is the bathymetry/topography map of
   ETOPO (called by using the :py:func:`mpl_toolkits.basemap.Basemap.etopo` function). If set
   to :samp:`Map Background`, the map background chosen by the user
   (using the :guilabel:`Background/Load background` file item) is plotted
   (as shown for instance in :numref:`fig_ihmsec2`). If no
   background file is provided, a DialogBox is opened, warning the user
   that no files has been loaded. And the :samp:`Filled Continents` mode
   is used instead.
#. When the plot mode is set to :samp:`Map Background`, the
   :guilabel:`clim` TextControl widget allow to change the colorbar upper
   and lower limits. 21 contours are plotted between the lower and
   upper colorbar limits.
#. When the plot mode is set to :samp:`Map Background`, the
   :guilabel:`colormap` ComboBox allows to change the colormap used in the
   filled contour. All the default matplotlib colorbars can be used.

.. _fig_ihmsec1:

.. figure:: _static/figs/sections_1.png
   :scale: 40 %

   GUI of the :py:mod:`pypago.guis.gui_sections_edition` program

.. _fig_ihmsec2:

.. figure:: _static/figs/sections_2.png
   :scale: 40 %

   Example of a map background (here, the GEBCO08 bathymetric chart)

Section definition
==================

When we have selected the domain of interest and the proper map
background, sections can either be created or edited, depending on the
values of the RadioBox :guilabel:`Choose the edition mode`.

New sections
-------------

If the :guilabel:`Choose the edition mode` RadioBox is on the
:guilabel:`Add sections` item, the user may define new sections.
Note that when this mode is activated, the map cannot be edited anymore.

Section endpoints are added by left-clicks on the map, as shown in
figure :numref:`fig_sections_3`. The section is then validated by a
right-click, allowing another
section to be added. By default, the sections are named
:samp:`section1`, :samp:`section2`, :samp:`section3` and so on. Sections
can also be created by simply entering the section coordinates in the
TextControl widgets (the :kbd:`ENTER` key must be pressed). 

.. warning:: 

    Note that the longitudes and latitudes must be separated by ",".

When all
the sections have been defined and validated, they must be
edited. This is done by switching :guilabel:`Choose the edition mode`
RadioBox to :guilabel:`Edit sections`.

.. _fig_sections_3:

.. figure:: _static/figs/sections_3.png
   :scale: 40 %

   Example of section creation.

Section edition
---------------

When the :guilabel:`Choose the edition mode` RadioBox is on the
:guilabel:`Edit sections` mode, the user may edit the defined sections
(i.e. change the section names, positions and segment directions).
The section that have been validated are drawn in thick black lines.

As a first step, the user must chose a section to edit. This is achieved by
clicking on one of the line. When done, the sections endpoints appear
as orange filled circles, the name of the section appears in the
:guilabel:`Section name` TextControl widget, the section coordinates appear
in the :guilabel:`Lon. coord.` and :guilabel:`Lat. coord.` TextControl widgets
and the
different segments of the segments are shown (:numref:`fig_sections_4`).

The user can change the name of the section as well as the section
longitude and latitude coordinates. This is done by modifying the text in
the :guilabel:`Section name`, :guilabel:`Lon. coord.` and
:guilabel:`Lat. coord.` TextControl widgets.
The changes must be validated by pressing the :kbd:`ENTER` key in the widget.
The position of the section can also be modified by a "click and drag" on
the section endpoints.

A critical step in the use of |pypago| is the definition of the
orientations of the sections (i.e. the direction where the transport
is counted positive), which must be carefully checked out by the
user. 
By default, all the sections have their segments oriented North-Eastward. The user must therefore set
the right orientations.
This is achieved by clicking on one of the segment number, as shown in
:numref:`fig_sections_4`.
Then, the user is able to change the orientation of the section by changing
the value of the :guilabel:`Segment #N` ComboBox (with N the number of
the segment).
Available orientations are North-East (:guilabel:`NE`),
North-West (:guilabel:`NW`), South-East (:guilabel:`SE`) and
South-West (:guilabel:`SW`).

Selected sections can also be deleted after a click on the
:guilabel:`Delete` button.

.. _fig_sections_4:

.. figure:: _static/figs/sections_4.png
   :scale: 40 %

   Example of section edition.

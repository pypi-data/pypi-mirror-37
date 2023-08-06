.. _loaddata:

Loading model data outputs
##########################

When the model section gridfile has been generated (and eventually the model domain file), 
the user can now load the model outputs.


Loading section data
********************

Loading data on sections is achieved by using the :py:func:`pypago.data.loaddata_sec_T` and :py:func:`pypago.data.loaddata_sec_UV` functions, depending
of the grid (T, U or V) in which the variable is stored.


Loading sections from T points
==============================

Loading sections from T points is achieved by using the :py:func:`pypago.data.loaddata_sec_T` function.

Its arguments are i) the list of :py:class:`pypago.sections.GridSection` objects ii) the NetCDF filename containing the variables to process iii) a dictionnary containing the variables to process (dictionnary values) and the name in which they will appear in the output object (dictionary keys). In the example below, the :samp:`votemper` and the :samp:`vosaline` variables are read from the input file and are stored as :samp:`temp` and :samp:`sal` attributes, respectively.

Loading sections from UV points
===============================

Loading sections from U/V points is achieved by using the :py:func:`pypago.data.loaddata_sec_UV`

Its arguments are i) the list of :py:class:`pypago.sections.GridSection` objects ii) the names of the NetCDF files containing the variables on the U and V points iii) a dictionnary containing the two names of the variables to process (dictionnary values, *which is a list* since the variable may have two different names depending of the file) and the name in which the variable will appear in the output object (dictionary keys). 
In the example below, we process the velocity field, whose name is uo in the grid U file and vo in the grid V file. This velocity field will be stored as
the vel attribute.

.. note::
    
    If in your model run, tracer transports (for instance heat transport) have been stored on U/V points, you may use this function to extract them. It gives better precision when computing heat budgets within closed
    domains.

Loading time
===============================

Loading the NetCDF time is achieved by using the :py:func:`pypago.data.loadtime` function (which uses the :py:func:`pypago.pyio.read_time` function) as follows:

The time is added as a time attribute. 

.. note::
    The name of the time variable is specified in the :file:`param.py` file

Example
===============

.. literalinclude::
    ../examples/loaddata_sections.py

.. ipython:: python

    import pypago.pyio
    data = pypago.pyio.load('data/indian_datasec.pygo')
    print(data[0])

Loading domain data
*******************

Loading data
===============================

Loading data on domain areas is achieved by using the :py:func:`pypago.data.loaddata_area_T` function.
The philosophy is the same as when loading section data from T points. However, a major difference is that here, 2D variables (for instance, surface heat fluxes) can be loaded. In the above example, the 3D (time, latitude, longitude) :samp:`votemper` and :samp:`vosaline` variables are loaded as :samp:`temp` and :samp:`salt`, respectively, while the 2D variable :samp:`sohefldo` is loaded as :samp:`hf`.


Loading time
===============================
Time is loaded as for sections, i.e. by using the :py:func:`pypago.data.loadtime` function.


Example
===============================

.. literalinclude::
    ../examples/loaddata_areas.py

.. ipython:: python

    import pypago.pyio
    data = pypago.pyio.load('data/natl_datadom.pygo')
    print(data[0])

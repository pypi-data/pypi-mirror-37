Parameter file
##################

The working of |pypago| is based on a Python parameter file, which contains the variables needed by the program. **The default parameter file (dedicated to the analysis of the NEMO model) is shown below.**

Prior to run |pypago| analysis, the user is requiered to create, in the working directory, a `param.py` file, which will overwrite these default parameters. 

The most critical variable is the :samp:`dictvname` directory, which contains the names of the coordinate and scale factor variables and which will dictate the behaviour of |pypago|, as detailed below.

.. warning::

    The variables defined in the :samp:`dictvname` dictionnary are required and must all be included in a unique file (:samp:`mesh_mask.nc` for instance).

.. literalinclude:: ../examples/sample_params/param_nemo.py

NEMO model 
-----------------

.. _table_nemo_var:
.. table:: Grid variables for the NEMO model
    
    .. csv-table::
            :header: Variable, Name, Description
            :file: _static/csv/nemo_model_des.csv

Recontruction of the bathymetry
+++++++++++++++++++++++++++++++++
If the :samp:`bathy_varname` is :samp:`None`, bathymetry is reconstructed from the :samp:`depth_varname` and the :samp:`mbathy_varname` variables

Recontruction of the vertical scale factors
++++++++++++++++++++++++++++++++++++++++++++
The reconstruction of the vertical scale factors depend on the shape of the :samp:`dzt` variable.

- If it is 1D, it is assumed that there are no partial steps, and :samp:`dzt` is tiled along the longitude and latitude dimensions. And the :samp:`dzw` and `dzn` variables are set equal to :samp:`dzt`. 
- If it is 2D, then a 3D :samp:`dzt` variable is reconstructed by using the :func:`pypago.coords.NemoCoords.create_3d_e3t` function. This function needs the 1D scale factor variable, whose name is defined by the :samp:`dzt1d_varname` variable. Then, if the :samp:`dze_varname` and :samp:`dzn_varname` variables are not :samp:`None`, these variables are read. Else, they are reconstructed from the 3D :samp:`dzt` variable by using the :func:`pypago.coords.NemoCoords.reconstruct_3d_e3uv` function. Finally, the :samp:`dzw` variable is reconstructed from the :samp:`dze` variable.

ROMS model 
-----------------

.. _table_roms_var:
.. table:: Grid variables for the ROMS model
    
    .. csv-table::
            :header: Variable, Name, Description
            :file: _static/csv/roms_model_des.csv

Reconstruction of horizontal scale factors
+++++++++++++++++++++++++++++++++++++++++++++++

In ROMS model, U points are located on the western faces, while V points are located on the southern faces. Therefore, the :samp:`dzn` variable is reconstructed by shifting the :samp:`dzs` variable.

Recontruction of the vertical scale factors
++++++++++++++++++++++++++++++++++++++++++++

Since ROMS is a :math:`\sigma` model, vertical scale factors is set equal to 1. Since the number of :math:`\sigma` levels 
is stored in the data file, the user has to define it in the :samp:`param.py` file so that the :samp:`dzt`, :samp:`dzn` and :samp:`dzw` variables are defined with the right dimensions.

.. todo:: 

    Complete for all the other models

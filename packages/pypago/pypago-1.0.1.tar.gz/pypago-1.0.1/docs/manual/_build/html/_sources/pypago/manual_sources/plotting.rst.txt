Plotting
##################################################

Drawing gridded sections
*********************************

The drawing of gridded sections is achived by using the :py:func:`pypago.plot.plot_dom_mask` function. It is done as follows:

.. literalinclude:: 
    ../examples/plot_dom_mask.py

.. ipython:: python 

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/plot_dom_mask.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. figure:: _static/figs/plot_dom_mask.png
    :align: center
    
    Results of grid, gridded section and domain plotting


Drawing data sections
*********************************

The drawing of data on gridded sections is 
achived by using the :py:func:`pypago.plot.pcolplot` (for *pcolor* plots) and 
:py:func:`pypago.plot.contourplot` functions. It is done as follows:

.. literalinclude:: 
    ../examples/plot_section_data.py

.. ipython:: python 

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/plot_section_data.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. figure:: _static/figs/section_temp.png
    :align: center
    
    Plotting of mean temperature on gridded section

.. figure:: _static/figs/section_vel.png
    :align: center
    
    Plotting of mean velocity on gridded section

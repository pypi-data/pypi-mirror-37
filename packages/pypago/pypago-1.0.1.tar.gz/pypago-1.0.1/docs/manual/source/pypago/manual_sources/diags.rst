Scientific diagnostics
##################################################

.. warning::

    These functions work, at this time, only for z-coordinate models (NEMO for instance). But
    they can provide some ideas on diagnostics.

Section transports
*********************************

The :py:mod:`pypago.secdiag` module contains several functions to compute transport across gridded sections. 

.. note::

    The total tracer transport must be equal to overturning + barotropic + baroclinic tracer 
    transports: TOT = OVT + BAR + BC
    
A complete example of transport calculations is shown below:

.. literalinclude:: 
    ../examples/section_transport.py

.. ipython:: python 

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/section_transport.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. figure:: _static/figs/heat_transport.png
    :align: center
    
    Example of heat transport calculations.

.. _budgets_calc:

Volume/Surface integration over domains
*******************************************

The :py:mod:`pypago.areadiag` module contains several functions in order to perform volume and surface integrations. These functions can be used for instance to tracer budgets calculations
over closed domains

In the example below, a heat budget calculation is performed over a closed domain, as in :cite:`Barrier2015`. It is based on the following equations:

.. math::
      :label: eqn_hb1

      h_c = \rho_0 C_p \left(\iiint_V T\ dx\ dy\ dz + \iint_{S_a} SST\ \eta\ dx\ dy \right) 

with :math:`\rho_0` and :math:`C_p` the reference density and heat capacity of
sea-water, :math:`T` the three-dimensional temperature, :math:`S_a` the
surface of the water volume :math:`V` that is in contact with the atmosphere, :math:`SST` and :math:`\eta`  the sea-surface temperature and
sea-surface height.with :math:`\rho_0` and :math:`C_p` the reference density and heat capacity of
sea-water, :math:`T` the three-dimensional temperature, :math:`S_a` the
surface of the water volume :math:`V` that is in contact with the atmosphere,
:math:`SST` and :math:`\eta` the sea-surface temperature and
sea-surface height.

.. math::
      :label: eqn_hb2

      \frac{\partial h_c}{\partial t} = {\iint_{S_a} Q_{net}\ dx\ dy}+{\rho_0 C_p \iint_{S_{o}} [U T]\ dl\  dz} + \varepsilon

with  :math:`Q_{net}` the net (latent, sensible, shortwave and longwave)
surface heat fluxes, :math:`S_o` the outline surface of volume :math:`V`  and :math:`[UT]` the ocean heat transport. The first term on the right-hand side of
equation :eq:`eqn_hb2` represents the contribution of surface heat fluxes to
changes in ocean heat content. In the following, a positive
contribution implies that the ocean is warmed by the atmosphere
(i.e. surface heat fluxes are, by convention, positive downwardwith  :math:`Q_{net}` the net (latent, sensible, shortwave and longwave)
surface heat fluxes, :math:`S_o` the outline surface of volume :math:`V`  and :math:`[UT]` the ocean heat transport. The first term on the right-hand side of
equation :eq:`eqn_hb2` represents the contribution of surface heat fluxes to
changes in ocean heat content. In the following, a positive
contribution implies that the ocean is warmed by the atmosphere
(i.e. surface heat fluxes are, by convention, positive downward)

.. literalinclude:: 
    ../examples/area_diags.py

.. ipython:: python 

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/area_diags.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. figure:: _static/figs/heat_budget.png
    :align: center
    
    Example of heat transport calculations.

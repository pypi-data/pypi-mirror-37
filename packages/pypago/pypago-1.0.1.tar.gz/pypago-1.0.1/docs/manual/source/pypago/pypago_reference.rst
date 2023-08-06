|pypago| reference manuals
==========================

.. warning::

   The list here may not be complete. Please refer to the index.

   At the end, this page should give quick access to end-users modules.

..
   to complete the list, here is a bash command to get useful modules
   of pypago/pypago_*/ in the right format

   .. code-block:: bash

      find ../../pypago/pypago_* -name "[a-z|A-Z]*.py" | sort | sed -e "s/.py$//" -e "s@\.\./\.\./@   @" -e "s@/@.@g"

   directories (aka packages) are also have to be added

   .. code-block:: bash

      find ../../pypago/pypago_* -type d | sort | sed -e "s@\.\./\.\./@   @" -e "s@/@.@g"

   to explicitly add private modules (prefix one hyphen) :

   .. code-block:: bash

      find ../../pypago/pypago_* -name "_[a-z|A-Z]*.py" | sort | sed -e "s/.py$//" -e "s@\.\./\.\./@   @" -e "s@/@.@g"

   only private module __param__.py has to be added:

   .. code-block:: bash

      find ../../pypago -name "__param__.py" | sort | sed -e "s/.py$//" -e "s@\.\./\.\./@   @" -e "s@/@.@g"

.. autosummary::
   :toctree: generated

        pypago.toolsec
        pypago.nc
        pypago.disp
        pypago.mat
        pypago.sections
        pypago.grid
        pypago.coords
        pypago.data
        pypago.coords
        pypago.plot
        pypago.areas
        pypago.misc
        pypago.pyio
        pypago.bin

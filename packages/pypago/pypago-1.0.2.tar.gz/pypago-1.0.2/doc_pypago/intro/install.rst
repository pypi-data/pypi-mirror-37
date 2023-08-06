
Installation
======================

Using subversion
###############################

Download the code
**********************

The code is hosted on a SVN repository. It can be downloaded as follows:

.. code-block:: none

    svn checkout https://subversion.renater.fr/pago/trunk

The code can be updated as follows:

.. code-block:: none

    svn update

Install the code
**********************

In your :samp:`.bashrc` file, add the destination directory to your :samp:`PYTHONPATH`:

.. code-block:: none

    export PYTHONPATH=$PYTHONPATH:/home/nbarrier/Bureau/test_pypago/lib/python

.. note::
    
    You must add  :samp:`lib/python` at the end of your destination directory

Then, from the :samp:`pago` directory, run the :samp:`setup.py` file as follows:

.. code-block:: none

    python setup.py install --home=/home/nbarrier/Bureau/test_pypago

Finally, in your :samp:`.bashrc` file, add the location of the :samp:`bin` directory to your :samp:`PATH`:

.. code-block:: none

    export PATH=$PATH:/home/nbarrier/Bureau/test_pypago/bin    

The latter will allow you to run the different executable scripts that come with |pypago|


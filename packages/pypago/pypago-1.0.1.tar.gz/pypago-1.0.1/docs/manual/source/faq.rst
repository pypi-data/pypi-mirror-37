===
FAQ
===

How can I see |pypago| version ?
++++++++++++++++++++++++++++++++

Like all Pyhton modules, if :envvar:`PATH` or  envvar:`PYTHONPATH` is
set, :command:`pydoc` is your friend:

.. code-block:: bash

   pydoc pypago

A more concise output here:

.. code-block:: bash

   python -c 'import pypago; print(pypago.__version__); print(pypago.__file__)'

The answer should look :

.. parsed-literal::

   2.0.0
   pypago/__init__.pyc

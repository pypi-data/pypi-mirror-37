======
ragavi
======

Radio Astronomy Gain and Visibility Inspector


============
Introduction
============

This library mainly requires
    1. Bokeh
    2. Nodejs for js
    3. casacore-dev

**- Install build dependencies:**

.. code-block:: bash
    
    $ apt-get install nodejs, casacore-dev

All python requirements are found in requirements.txt

or
 
To install nodejs in the virtual environment, use: nodeenv, a nodejs virtual environment.
More info can be found here_

Create nodejs virtual environment with:

.. code-block:: bash
    
    $ nodeenv envName

and

.. code-block:: bash

    $ . envName/bin/activate

to switch to environment. 

============
Installation
============

Installation from source_,
working directory where source is checked out

.. code-block:: bash
  
    $ pip install .

This package will soon be available on *PYPI*, allowing

.. code-block:: bash
      
     $ pip install ragavi

=======
License
=======

This project is licensed under the MIT License - see license_ for details.

===========
Contribute
===========

Contributions are always welcome! Please ensure that you adhere to our coding standards pep8_.

.. _here: https://pypi.org/project/nodeenv
.. _source: https://github.com/ratt-ru/ragavi
.. _pep8: https://www.python.org/dev/peps/pep-0008
.. _license: https://github.com/ratt-ru/ragavi/blob/master/LICENSE

Installation
############

``yafe`` requires the following packages:

* `python >= 3.5 <https://wiki.python.org/moin/BeginnersGuide/Download>`_
* `numpy >= 1.13 <http://www.numpy.org>`_

Optionnaly, `xarray >= 0.10 <http://xarray.pydata.org>`_ is needed to be able
to load the results as labeled arrays with the method
:meth:`~yafe.base.Experiment.load_results`.

Make sure your Python environment is properly configured. It is recommended to
install ``yafe`` in a virtual environment.

Release version
---------------

First, make sure you have the latest version of pip (the Python package
manager) installed. If you do not, refer to the `Pip documentation
<https://pip.pypa.io/en/stable/installing/>`_ and install ``pip`` first.

Install the current release with ``pip``::

    pip install yafe

To upgrade to a newer release use the ``--upgrade`` flag::

    pip install --upgrade yafe

If you do not have permission to install software systemwide, you can install
into your user directory using the ``--user`` flag::

    pip install --user yafe

Alternatively, you can manually download ``yafe`` from its `GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/yafe>`_  or `PyPI
<https://pypi.python.org/pypi/yafe>`_.  To install one of these versions,
unpack it and run the following from the top-level source directory using the
Terminal::

    pip install .

The :mod:`yafe` package uses a configuration file to specify some default
paths. To learn how to create this file before using :mod:`yafe`, see the
corresponding section :ref:`yafe_configuration_file`.

Development version
-------------------

If you have `Git <https://git-scm.com/>`_ installed on your system, it is also
possible to install the development version of ``yafe``.

Before installing the development version, you may need to uninstall the
standard version of ``yafe`` using ``pip``::

    pip uninstall yafe

Clone the Git repository::

    git clone git@gitlab.lis-lab.fr:skmad-suite/yafe.git
    cd yafe

You may also need to install required packages::

    pip install -r requirements/defaults.txt

Then execute ``pip`` with flag ``-e`` to follow the development branch::

    pip install -e .

To update ``yafe`` at any time, in the same directory do::

    git pull

To run unitary tests, first install required packages::

    pip install -r requirements/dev.txt

and execute ``pytest``::

    pytest


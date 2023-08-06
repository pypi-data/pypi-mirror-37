#########################
:mod:`yafe` documentation
#########################

Overview
========
:mod:`yafe`: Yet Another Framework for Experiments.

A classical workflow consists in the following steps:

* load some data,
* generate a problem from the data,
* solve the problem,
* compute performance criteria,
* display results.

Experiments are then conducted by repeating this task while varying the
data, problem parameters, solvers and/or solver parameters. A computer
cluster may be used to run all the resulting tasks in parallel,
which requires to distribute them adequately among the available
resources and then to collect and merge the results.

The package :mod:`yafe` offers a generic framework to conduct such experiments,
aiming at saving time and avoiding errors:

* the generic framework facilitates the design of experiments,
* convenient data structures help to handle results quickly and without
  confusion between multiple dimensions,
* intermediate results can be tracked,
* tasks are computed once, even when new tasks are added.

Documentation
=============

.. only:: html

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 1

    installation
    references
    tutorials
    credits


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

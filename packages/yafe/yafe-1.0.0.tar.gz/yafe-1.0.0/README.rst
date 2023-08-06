yafe
====

yafe: Yet Another Framework for Experiments.

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

The package `yafe` offers a generic framework to conduct such experiments,
aiming at saving time and avoiding errors:

* the generic framework facilitates the design of experiments,
* convenient data structures help to handle results quickly and without
  confusion between multiple dimensions,
* intermediate results can be tracked,
* tasks are computed once, even when new tasks are added.


Install
-------

Install the current release with ``pip``::

    pip install yafe

For additional details, see doc/install.rst.

Usage
-----

See the `documentation <http://skmad-suite.pages.lis-lab.fr/yafe/>`_.

Bugs
----

Please report any bugs that you find through the `yafe GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/yafe/issues>`_.

You can also fork the repository and create a merge request.

Source code
-----------

The source code of yafe is available via its `GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/yafe>`_.

You can clone the git repository of the project using the command::

    git clone git@gitlab.lis-lab.fr:skmad-suite/yafe.git

Copyright © 2017-2018
---------------------

* `Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>`_
* `Université d'Aix-Marseille <http://www.univ-amu.fr/>`_
* `Centre National de la Recherche Scientifique <http://www.cnrs.fr/>`_
* `Université de Toulon <http://www.univ-tln.fr/>`_

Contributors
------------

* `Ronan Hamon <mailto:ronan.hamon@lis-lab.fr>`_
* `Valentin Emiya <mailto:valentin.emiya@lis-lab.fr>`_
* `Florent Jaillet <mailto:florent.jaillet@lis-lab.fr>`_

License
-------

Released under the GNU General Public License version 3 or later
(see `LICENSE.txt`).

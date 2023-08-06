# -*- coding: utf-8 -*-
"""Example experiment to be deployed on a cluster grid with OAR.

.. moduleauthor:: Ronan Hamon
.. moduleauthor:: Valentin Emiya
.. moduleauthor:: Florent Jaillet

This example and the following workflow illustrates the design of a ``yafe``
experiment, its execution on a cluster and how to collect and exploit
results remotely or locally.

* On the cluster frontend, run this script to generate the experiment,
  its tasks, and the OAR script (see ``__main__`` below). Note that if you are
  using a virtual environment, you should add it as an argument when calling
  function ``generate_oar_script`` and activate it before running this script.

* Run the tasks on the cluster by executing the command line displayed by
  the script.

* Optionally, collect and exploit results on the cluster by opening a python
  session and by running::

      from example_oar import experiment
      experiment.collect_results()
      results, axes_labels, axes_values = experiment.load_results()

* In order to exploit results on a local machine, download the
  experiment directory and all its contents into your local data path and
  run the above code locally. Note that downloading all the directory
  is needed to preserve the consistency of the task indexing, especially if
  you want to examine some specific tasks or add new ones.

* If you only want to exploit results without downloading all the
  experiment data stored in the directory, you should collect the
  results remotely on the cluster and download files ``_schema.pickle`` and
  ``results.npz`` into your local data directory. You can then exploit the
  results using ::

      from example_oar import experiment
      results, axes_labels, axes_values = experiment.load_results()

  Be aware that only the method ``load_results`` will be usable and that the
  ``experiment`` object will be in an inconsistent state for all the other
  methods.
"""
import numpy as np

from yafe import Experiment
from yafe.utils import generate_oar_script


def get_sine_data(f0, signal_len=1000):
    return {'signal': np.sin(2*np.pi*f0*np.arange(signal_len))}


class SimpleDenoisingProblem:
    def __init__(self, snr_db):
        self.snr_db = snr_db

    def __call__(self, signal):
        random_state = np.random.RandomState(0)
        noise = random_state.randn(*signal.shape)
        observation = signal + 10 ** (-self.snr_db / 20) * noise \
            / np.linalg.norm(noise) * np.linalg.norm(signal)
        problem_data = {'observation': observation}
        solution_data = {'signal': signal}
        return problem_data, solution_data

    def __str__(self):
        return 'SimpleDenoisingProblem(snr_db={})'.format(self.snr_db)


class SmoothingSolver:
    def __init__(self, filter_len):
        self.filter_len = filter_len

    def __call__(self, observation):
        smoothing_filter = np.hamming(self.filter_len)
        smoothing_filter /= np.sum(smoothing_filter)
        return {'reconstruction': np.convolve(observation, smoothing_filter,
                                              mode='same')}

    def __str__(self):
        return 'SmoothingSolver(filter_len={})'.format(self.filter_len)


def measure(solution_data, solved_data, task_params=None, source_data=None,
            problem_data=None):
    euclidian_distance = np.linalg.norm(solution_data['signal']
                                        - solved_data['reconstruction'])
    sdr = 20 * np.log10(np.linalg.norm(solution_data['signal'])
                        / euclidian_distance)
    inf_distance = np.linalg.norm(solution_data['signal']
                                  - solved_data['reconstruction'], ord=np.inf)
    return {'sdr': sdr,
            'euclidian_distance': euclidian_distance,
            'inf_distance': inf_distance}


def create_tasks(exp):
    data_params = {'f0': np.arange(0.01, 0.1, 0.01), 'signal_len': [1000]}
    problem_params = {'snr_db': [-10, 0, 30]}
    solver_params = {'filter_len': 2**np.arange(6, step=2)}
    exp.add_tasks(data_params=data_params,
                  problem_params=problem_params,
                  solver_params=solver_params)
    exp.generate_tasks()


experiment = Experiment(name='yafe_oar_example',
                        get_data=get_sine_data,
                        get_problem=SimpleDenoisingProblem,
                        get_solver=SmoothingSolver,
                        measure=measure)


if __name__ == '__main__':
    create_tasks(experiment)
    generate_oar_script(script_file_path=__file__,
                        xp_var_name='experiment',
                        batch_size=4,
                        oar_walltime='00:05:00')

#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
18.04.2018

Description: Contains the experiment handler, a class that organizes experiments.
"""

import EthIefLab.KillableThread as KillableThread


class ExperimentHandler(object):
    """
    Handles experiments. Starts separate thread to run experiment and notifies if the experiment has finished.
    """

    @property
    def current_experiment(self):
        """
        Gets the current experiment.
        :return: current experiment
        """
        return self._current_experiment

    @current_experiment.setter
    def current_experiment(self, experiment):
        """
        Sets the current experiment.
        :param experiment: experiment to set
        """
        self.stop_experiment()  # stop old experiment if it is still running
        self._current_experiment = experiment  # replace experiment
        self._experiment_thread = None         # remove experiment thread

    def __init__(self):
        self._experiment_thread = None
        self._current_experiment = None
        self.experiment_finished = list()   # initialize structure for callbacks

    def __run__(self):
        """Worker function for the experiment thread."""
        self._current_experiment.run(self) # run experiment

        # execute callback functions
        for callback in self.experiment_finished:
            callback()

        print('Experiment Finished.')

    def run_experiment(self, experiment = None):
        """
        Run experiment. Either runs current experiment or sets the current experiment according to the parameters.
        :param experiment: experiment to run (overwrites current_experiment)
        """
        if experiment is None:
            experiment = self.current_experiment

        if not experiment is None:
            self._experiment_thread = KillableThread(target=self.__run__)  # create a killable thread for the experiment
            self._experiment_thread.start()    # start experiment thread

    def stop_experiment(self):
        """
        Stop current experiment (should be used primarily in case of an emergency)
        """
        if not self._experiment_thread is None and not self._current_experiment is None:
            self._experiment_thread.terminate()

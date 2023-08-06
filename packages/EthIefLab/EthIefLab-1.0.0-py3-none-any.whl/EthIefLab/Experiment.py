#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
18.04.2018

Description: Contains the base class that each experiment inherits.
"""

import EthIefLab.ObservableList as ObservableList
from tkinter import messagebox, Tk


def message(text, title=None, message_type='info'):
    """
    Displays a message box.
    :param text: text to show in the message box
    :param title: title of the message box
    :param message_type: type of the message box
    """
    if message_type == 'error':
        messagebox.showerror(title, text)
    elif message_type == 'warning':
        messagebox.showwarning(title, text)
    else:
        messagebox.showinfo(title, text)


class Experiment(object):
    """
    This is the base class for all experiments which can be executed with the tool.
    """

    def __init__(self):
        self.plot_collection = ObservableList()
        self.parameters = None

    def run(self, handler):
        """
        This method has to be implemented.
        :param handler: The handler that runs the experiment.
        """
        raise NotImplemented()
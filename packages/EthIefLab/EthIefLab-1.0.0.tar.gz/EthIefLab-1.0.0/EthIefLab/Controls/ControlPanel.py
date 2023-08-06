#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
18.04.2018

Description: Contains the definition for the control panel.
"""

from tkinter import Button, NORMAL, DISABLED
from .CustomFrame import CustomFrame
#import EthIefLab.Controls.CustomFrame


class ControlCommand(object):
    """
    This object is used as an item in the the control panel. It contains the command can can be enabled or disabled.
    """
    _can_execute = True

    @property
    def can_execute(self):
        """
        Gets if this command can be executed (if false the associated button will be grayed out)
        :return: true or false
        """
        return self._can_execute

    @can_execute.setter
    def can_execute(self, b):
        """
        Sets if this command can be executed (will gray out associated button if set to False)
        :param b: True or False
        """
        self._can_execute = b
        if not self.button_handle is None:
            self.button_handle.config(state=NORMAL if self._can_execute else DISABLED)

    _button_handle = None

    @property
    def button_handle(self):
        """
        Gets the associated button object
        :return: widget
        """
        return self._button_handle

    @button_handle.setter
    def button_handle(self, handle):
        """
        Sets the associated button object
        :param handle: widget
        """
        self._button_handle = handle
        self.can_execute = self._can_execute

    def __init__(self, command, name='', can_execute=True):
        self.name = name
        self.command = command
        self.can_execute = can_execute


class ControlPanel(CustomFrame):
    """
    This frame will be populated by buttons if a list of ControlCommands is set as its command_source.
    """

    _command_source = None

    @property
    def command_source(self):
        """
        Gets the command source of this control panel.
        :return: list of type ControlCommand
        """
        return self._command_source

    @command_source.setter
    def command_source(self, source):
        """
        Sets the command source. (Will produce buttons for each command in the source)
        :param source: list of type ControlCommand
        """
        self._command_source = source
        self.__setup__()

    _button_width = None

    @property
    def button_width(self):
        """
        Gets the fixed with of all the buttons in the control panel.
        :return: width of buttons
        """
        return self._button_width

    @button_width.setter
    def button_width(self, width):
        """
        Sets the width of all the buttons on the control panel.
        :param width: width of the buttons
        """
        self._button_width = width
        self.__setup__()

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._root = parent
        self.__setup__()

    def __setup__(self):
        self.clear()

        if self._command_source is None:
            return

        r = 0
        for command in self._command_source:
            command.button_handle = self.add_widget(Button(self, text=command.name, command=command.command),
                                                    row=r, padx=10, pady=5)

            if not self._button_width is None:
                command.button_handle.config(width=self._button_width)

            r += 1

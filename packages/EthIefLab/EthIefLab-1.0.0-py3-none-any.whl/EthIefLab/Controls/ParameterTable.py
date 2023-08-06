#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
18.04.2018

Description: The parameter table generates a visually structured table of input parameters for the user to configure
them.

"""

from tkinter import DoubleVar, StringVar, BooleanVar, Label, Entry, Checkbutton, filedialog, Button
from .CustomFrame import CustomFrame
import json
import os


class ConfigParameter(object):
    """
    Handles parameters for parameter tables.
    As a basis the tkinter.Variables are used which notify the ui about changes automatically.
    """

    @property
    def value(self):
        """
        Gets the current value of the parameter.
        :return: value of the parameter
        """
        return self.variable.get()

    @value.setter
    def value(self, v):
        """
        Sets the current value of the parameter.
        :param v: value
        """
        self.variable.set(v)

    def __init__(self, parent, value=0, unit=None, parameter_type='number'):
        # initialize the parameter either as a number or as text
        if parameter_type == 'number':
            self.variable = DoubleVar(parent, value)
        elif parameter_type == 'bool':
            self.variable = BooleanVar(parent, value)
        else:
            self.variable = StringVar(parent, value)
        self.unit = unit
        self.parameter_type = parameter_type

    def browse_folders(self):
        """
        Open folder browser.
        """
        result = filedialog.askdirectory(initialdir=self.value)
        if result is not None and result != '':
            self.value = result

    def browse_files(self):
        """
        Open file browser.
        """
        result = filedialog.asksaveasfilename(initialdir=self.value)
        if result is not None and result != '':
            self.value = result


class ParameterTable(CustomFrame):
    """
    A UI control that creates a table from a given set of parameters so they can easily be set from the UI.
    """

    _parameter_source = None

    @property
    def parameter_source(self):
        """
        Gets the currently set parameter dictionary.
        :return: dictionary with ConfigParameter objects as values
        """
        return self._parameter_source

    @parameter_source.setter
    def parameter_source(self, source):
        """
        Sets the parameter dictionary.
        :param source: dictionary with the parameter names as keys and ConfigParameter objects as values
        """
        self._parameter_source = source
        self.__setup__()    # redraw the control with the new parameter source

    _show_apply_button = False

    @property
    def show_apply_button(self):
        """
        Gets if apply button is shown
        :return: True or False
        """
        return self._show_apply_button

    @show_apply_button.setter
    def show_apply_button(self, v):
        """
        Sets if apply button is shown
        :param v: True or False
        """
        self._show_apply_button = v
        self._apply_button.grid_forget()
        if self._show_apply_button:
            self._apply_button.grid(row=self._row_count, column=0, sticky='w', padx=2, pady=2)


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)   # call the parent class's constructor
        self._root = parent    # keep reference to the ui parent
        self.apply_command = None  # store command which gets executed when the apply button is clicked
        self._row_count = 0
        self.__setup__()        # draw the table

    def __setup__(self):
        self.clear()    # remove all existing ui controls from the table

        self._apply_button = Button(self, text='apply', command=self.__run_apply_command)
        self._children.append(self._apply_button)
        self.show_apply_button = self._show_apply_button

        if self.parameter_source is None:   # do nothing if no parameters are set
            return

        # add the fields for all the parameters
        r = 0
        for parameter_name in self.parameter_source:
            parameter = self.parameter_source[parameter_name]       # get the next parameter
            self.add_widget(Label(self, text='{}:'.format(parameter_name)), row=r, column=0, sticky='w')    # add parameter name

            if parameter.parameter_type == 'bool':
                self.add_widget(Checkbutton(self, variable=parameter.variable), row=r, column=1, sticky='w')
            else:
                self.add_widget(Entry(self, textvariable=parameter.variable), row=r, column=1, sticky='w')  # add entry to edit value

            if not parameter.unit is None:
                self.add_widget(Label(self, text='[{}]'.format(parameter.unit)), row=r, column=2, sticky='w')  # add unit description

            # add browse button for files and folders
            if parameter.parameter_type == 'folder':
                self.add_widget(Button(self, text='browse...',
                                       command=parameter.browse_folders), row=r, column=2, padx=5)
            if parameter.parameter_type == 'file':
                self.add_widget(Button(self, text='browse...',
                                       command=parameter.browse_files), row=r, column=2, padx=5)
            r += 1
        self._row_count = r

        self.show_apply_button = self._show_apply_button

    def __run_apply_command(self):
        if self.apply_command is not None:
            self.apply_command()

    def serialize(self, path):
        """
        Serializes data in table to json.
        :param path: path to save the serialized data to
        """
        if self._parameter_source is None:
            return
        data = {}
        for parameter_name in self._parameter_source:
            data[parameter_name] = self._parameter_source[parameter_name].value
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def deserialize(self, path):
        """
        Deserializes the table data from a given file and loads it into the cells.
        :param path: path where the file with the serialized data is located
        """
        if self._parameter_source is None or not os.path.isfile(path):
            return
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
        for parameter_name in data:
            self._parameter_source[parameter_name].value = data[parameter_name]
        self.__setup__()

#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
18.04.2018

Description: The custom frame provides an extension of the tkinter LabelFrame. It adds the ability to disable or enable
the entire content easily and it also allows to se the title of the frame easily. Furthermore it keeps track of its
child objects such that they can easily be cleared if the inheriting control needs to update.

"""

from tkinter import LabelFrame, NORMAL, DISABLED, BooleanVar, Frame


class CustomFrame(LabelFrame):
    """
    Extended version of the tkinter frame. Provides some useful, general functionality.
    """

    _title = ''

    @property
    def title(self):
        """
        Gets the title of the frame
        :return: title
        """
        return self._title

    @title.setter
    def title(self, txt):
        """
        Sets the title of the frame
        :param txt: title
        """
        self.config(text=txt)

    _enabled = True
    _enabled_var = None

    @property
    def enabled(self):
        """
        Gets if this control is enabled.
        :return: True or False
        """
        return self._enabled

    @enabled.setter
    def enabled(self, v):
        """
        Sets if this control is enabled.
        :param v: True or False
        """

        if type(v) is BooleanVar:   # check if tkinter variable was used
            self._enabled_var = v   # use variable to keep track of changes
            self._enabled_var.trace('w', self.__enabled_var_changed__)  # listen for changes
            v = v.get() # extract boolean value

        self._enabled = v
        for child in self._children:    # set state of all child objects
            if child is not None:
                if type(child) == Frame:    # frames do not have a state
                    continue
                child.config(state=(NORMAL if self._enabled else DISABLED))

    def __enabled_var_changed__(self, *args):
        self.enabled = self._enabled_var.get()

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)   # call the constructor of the parent class
        self._root = parent        # keep reference to ui parent
        self._children = []        # collection of all child controls that were added to the frame
        self.title = self._title   # set the title initially
        #self._enabled_var = BooleanVar(parent, True)

    def clear(self):
        """
        Remove all child ui controls from the frame.
        """
        for child in self._children:
            child.grid_forget()
        self._children = []

    def add_widget(self, widget, **kwargs):
        """
        Add child ui control to the frame and place it in the grid structure of the frame.
        :param widget: widget to add
        :param kwargs: arguments for positioning the widget inside the grid
        :return: widget that was added
        """
        widget.grid(**kwargs)
        self._children.append(widget)
        return widget

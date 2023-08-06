#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
24.04.2018

Description: The plot control allows to embed multiple matplotlib plots into the UI and update them very easily.

"""

import numpy as np
from tkinter import Frame, BOTTOM, BOTH, TOP
import EthIefLab.ObservableList as ObservableList
import matplotlib
from matplotlib.collections import PathCollection
#from matplotlib.backends.backend_qt4agg import FigureCanvasTkAgg, NavigationToolbar2QT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use('TkAgg')     # enable that plots can be embedded into widgets


class PlotData(object):
    """
    This holds the data for a plot. It contains the x and y values as well as the type of plot.
    Keeps track of changes: If x or y change it will alert the plot to update.
    """
    _x = None

    @property
    def x(self):
        """
        Gets the x values of the plot.
        :return: x values
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Sets the x values of the plot and updates them.
        :param value: x values (ideally given as ObservableList, this enables the plot control to update this plot
        automatically)
        """
        if type(self._x) is ObservableList:     # if the old value was observable stop listening for changes
            self._x.item_added.append(self.__item_changed__)
            self._x.item_removed.append(self.__item_changed__)
        if type(value) is ObservableList:   # if the value it observable start listening for changes
            value.item_added.append(self.__item_changed__)
            value.item_removed.append(self.__item_changed__)
        self._x = value
        self.__update__()

    _y = None
    @property
    def y(self):
        """
        Gets the y values of the plot.
        :return: y values
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Sets the y values of the plot and updates them.
        :param value: y values (ideally given as ObservableList, this enables the plot control to update this plot
        automatically)
        """
        if type(self._y) is ObservableList:      # if the old value was observable stop listening for changes
            self._y.item_added.append(self.__item_changed__)
            self._y.item_removed.append(self.__item_changed__)
        if type(value) is ObservableList:       # if the value is observable start listening for changes
            value.item_added.append(self.__item_changed__)
            value.item_removed.append(self.__item_changed__)
        self._y = value
        self.__update__()

    _text = None

    @property
    def text(self):
        """
        Gets the text of this plot.
        :return: plot text
        """
        return self._text

    @text.setter
    def text(self, txt):
        """
        Sets the text of this plot.
        :param txt: plot text
        """
        self._text = txt
        self.__update__()

    def __init__(self, x=None, y=None, text=None, plot_type='plot', **plot_args):
        self.data_changed = list()
        self.x = x
        self.y = y
        self.text = text
        self.plot_type = plot_type
        self.line_handle = None
        self.plot_args = plot_args
        self.plot_control = None

    def __item_changed__(self, item):
        """Gets called in case that x and y are observable and one of them has changed"""
        self.__update__()

    def __update__(self):
        for callback in self.data_changed:
            callback(self)


class PlotControl(Frame):
    """
    Displays a plot which can be controlled with a plot data collection. Tries to update plots according to changes
    in the source data.
    """
    _title = None

    @property
    def title(self):
        """
        Gets the title of the plot.
        :return: plot title
        """
        return self._title

    @title.setter
    def title(self, t):
        """
        Sets the title of the plot.
        :param t: plot title
        """
        self._title = t
        if not self.ax is None:
            if not self._title is None:
                self.ax.set_title(self._title)
            else:
                self.ax.set_title('')
        self.__update_canvas__()

    _hold = False

    @property
    def hold(self):
        """
        Gets if the plots should be overwritten when a new plot is added.
        :return: True or False
        """
        return self._hold

    @hold.setter
    def hold(self, h):
        """
        Sets if the plots should be overwritten when a new plot is added.
        :param h: True or False
        """
        self._hold = h
        if not self.ax is None:
            self.ax.hold = h

    _show_grid = False

    @property
    def show_grid(self):
        """
        Gets if the grid is being displayed.
        :return: True or False
        """
        return self._show_grid

    @hold.setter
    def show_grid(self, g):
        """
        Sets if the grid is being displayed.
        :param g: True or False
        """
        self._show_grid = g
        if not self.ax is None:
            if self._show_grid:
                self.ax.grid(color='k', linestyle='-', linewidth=0.5)
            else:
                self.ax.grid(color='k', linestyle='-', linewidth=0)
        self.__update_canvas__()

    _axis_limit_margin_fraction = 0.1

    @property
    def axis_limit_margin_fraction(self):
        """
        Gets the fraction of the axis span that is added before and after the data.
        (Only used if autoscale is enabled)
        :return: margin fraction
        """
        return self._axis_limit_margin_fraction

    @axis_limit_margin_fraction.setter
    def axis_limit_margin_fraction(self, h):
        """
        Sets the fraction of the axis span that is added before and after the data.
                (Only used if autoscale is enabled)
        :param h: margin fraction
        """
        self._axis_limit_margin_fraction
        self.__handle_scaling__()

    _data_source = None

    @property
    def data_source(self):
        """
        Gets the plot data source of this plot.
        :return: plot source list
        """
        return self._data_source

    @data_source.setter
    def data_source(self, source: ObservableList):
        """
        Sets the plot data source of this plot. (Will replace old plots if set)
        :param source: An observable list of PlotData. If the list changes the plots will be updated.
        """
        if not self._data_source is None:   # check if old data source is being used currently
            for item in self._data_source:  # iterate over old plot data items
                item.data_changed.remove(self.__item_changed__) # disconnect callback method from items
                if not item.line_handle is None: item.line_handle.remove()  # remove plot
            self._data_source.item_added.remove(self.__item_added__)      # remove callback to notify about plot removal
            self._data_source.item_removed.remove(self.__item_removed__)  # remove callback to notify about plot adding
            self._data_source.on_clear.remove(self.__source_cleared__)    # remove callback to clear event

        if source is None:  # if the new source is none do nothing
            return

        self._data_source = source  # set new source
        self._data_source.item_added.append(self.__item_added__)        # listen to add changes of the plot data source
        self._data_source.item_removed.append(self.__item_removed__)    # listen to remove changes
        self._data_source.on_clear.append(self.__source_cleared__)      # list to clear list event
        for item in self._data_source:
            item.data_changed.append(self.__item_changed__)     # listen to changes of all plot data items
            item.plot_control = self
        self.__plot_setup__()   # plot the currently available data

    def __init__(self, parent, add_toolbar=False, figsize=(5, 5), dpi=100, autoscale_axis=True):
        super(PlotControl, self).__init__(parent)   # call the parent controls constructor
        self._root = parent # keep a reference for the ui root
        self._toolbar = None
        self._enable_toolbar = add_toolbar  # member to store whether a plot toolbar should be added or not
        self._figsize = figsize             # figure size
        self._dpi = dpi                     # dpi resolution
        self.autoscale_axis = autoscale_axis    # True = automatically calculate the axis limits to include all data
        self.__setup__()                        # setup control

    def __setup__(self):
        self._figure = Figure(figsize=self._figsize, dpi=self._dpi)  # define plot size
        self.ax = self._figure.add_subplot(111)  # add subplot and save reference
        self.ax.hold = self._hold

        self._canvas = FigureCanvasTkAgg(self._figure, self)  # add figure to canvas
        self._canvas.draw()  # show canvas
        self._canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)  # place canvas

        if self._enable_toolbar:
            # A bug in tk prohibits the packaging of the toolbar currently -> tbd
            #self._toolbar = NavigationToolbar2Tk(self._canvas, self)  # enable plot toolbar
            #self._toolbar.update()  # update toolbar
            self._canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def __update_canvas__(self):
        self.__handle_scaling__()       # setup proper axis scaling
        self._canvas.draw()             # redraw canvas
        # self._canvas.flush_events()   # trigger UI update

    def __source_cleared__(self):
        """Remove old plot"""
        if self._toolbar is not None:
            self._toolbar.pack_forget()
        self._canvas.get_tk_widget().pack_forget()
        self.__setup__()

    def __item_added__(self, item: PlotData):
        """Gets called if a new plot data item is added to the plot data source."""
        self.__add_plot__(item)     # add plot to the canvas
        item.data_changed.append(self.__item_changed__)     # listen to data changes of this plot data item
        item.plot_control = self
        self.__update_canvas__()

    def __item_removed__(self, item: PlotData):
        """Gets called if a plot data item gets removed from the plot data source."""
        item.line_handle.remove()   # remove the plot from the canvas
        item.data_changed.remove(self.__item_changed__)     # stop listening to changes of this plot data item
        self.__update_canvas__()

    def __item_changed__(self, item: PlotData):
        """Gets called if a plot data item gets changed. (e.g. the y collection is overwritten with new data)"""
        if item.x is None or item.y is None:    # do nothing if either the x or y data is set to None
            return

        x_size = len(item.x)    # get size of x value collection
        y_size = len(item.y)    # get size of y value collection
        x_data = item.x         # get data for x axis
        y_data = item.y         # get data for y axis

        # make sure that x and y data are of equal size before the plot data is set
        if x_size > y_size:     # check if x data has more entries than y data
            x_data = ObservableList()
            for i in range(y_size): x_data.append(item.x[i])    # set x to equal size as y
        elif y_size > x_size:   # check if y data has more entries than x data
            y_data = ObservableList()
            for i in range(x_size): y_data.append(item.y[i])    # set y to equal size as x

        if type(item.line_handle) is PathCollection:    # check if the plot being used is a scatter plot (different)
            data = np.asarray([x_data, y_data]).transpose()     # prepare data such that it is compatible (2xN)
            item.line_handle.set_offsets(data)  # update scatter plot with new data
        else:   # other plot types
            item.line_handle.set_xdata(x_data)  # set x data
            item.line_handle.set_ydata(y_data)  # set y data
        self.__update_canvas__()

    def __plot_setup__(self):
        """Gets executed to draw all the plots if a plot source has been specified.
        If plots are being done manually this method is not used."""
        if self.ax is None: # do nothing if no base plot is present
            return

        self.hold = True    # enable hold option
        for plot_data in self._data_source:
            self.__add_plot__(plot_data)    # plot all the given plot data

        self.__update_canvas__()

    def __add_plot__(self, plot_data: PlotData):
        """Plots plot data according to their configuration."""
        x = plot_data.x
        y = plot_data.y

        if x is None: x = [0]   # handle none items -> would crash otherwise
        if y is None: y = [0]   # handle none items -> would crash otherwise

        if plot_data.plot_type == 'plot':
            plot_data.line_handle, = self.ax.plot(x, y, **plot_data.plot_args)
        elif plot_data.plot_type == 'scatter':
            plot_data.line_handle = self.ax.scatter(x, y, **plot_data.plot_args)
        elif plot_data.plot_type == 'text':
            plot_data.line_handle = self.ax.text(x, y, plot_data.text, **plot_data.plot_args)

    def __handle_scaling__(self):
        """If autoscaling is enabled this method defines the appropriate axis ranges."""
        if not self.autoscale_axis or self.ax is None or self._data_source is None or len(self._data_source) == 0:
            return  # do nothing if either autoscaling is disabled, plot is none or the data source is none

        first_iteration = True   # used for initialization of the extrema variables
        x_min, x_max, y_min, y_max = -1, 1, -1, 1   # definition of extrema variables
        for plot_data in self._data_source:     # check each plot for its maximum and minimum values on both axis
            if plot_data.x is None or plot_data.y is None:
                continue    # skip the plot if its data is not valid because there is no data
            length_x = len(plot_data.x) if hasattr(plot_data.x, '__len__') else 1   # do to prevent single value failure
            length_y = len(plot_data.y) if hasattr(plot_data.y, '__len__') else 1   # do to prevent single value failure
            if length_x == 0 or length_y == 0:
                continue    # skip the plot if there are no points
            cx_max = np.max(plot_data.x)    # get maximum x value
            cx_min = np.min(plot_data.x)    # get minimum x value
            cy_max = np.max(plot_data.y)    # get maximum y value
            cy_min = np.min(plot_data.y)    # get minimum y value

            # set all values in first iteration as comparison basis
            if cx_max > x_max or first_iteration:    # set new global maximum x value if the current value is higher
                x_max = cx_max
            if cx_min < x_min or first_iteration:    # set new global minimum x value if the current value is lower
                x_min = cx_min
            if cy_max > y_max or first_iteration:    # set new global maximum y value if the current value is higher
                y_max = cy_max
            if cy_min < y_min or first_iteration:    # set new global minimum y value if the current value is lower
                y_min = cy_min

            first_iteration = False  # now we aren't in the first iteration anymore

        dx = x_max - x_min  # get x axis span
        dy = y_max - y_min  # get y axis span
        if dx == 0: dx = self._axis_limit_margin_fraction   # if span is zero set it to a small margin
        if dy == 0: dy = self._axis_limit_margin_fraction   # if span is zero set it to a small margin
        x_min -= dx * self._axis_limit_margin_fraction      # add margin to x axis minimum
        x_max += dx * self._axis_limit_margin_fraction      # add margin to x axis maximum
        y_min -= dy * self._axis_limit_margin_fraction      # add margin to y axis maximum
        y_max += dy * self._axis_limit_margin_fraction      # add margin to y axis minimum

        self.ax.set_xlim([x_min, x_max])    # set x axis range including the defined margin before and after the data
        self.ax.set_ylim([y_min, y_max])    # set y axis range including the defined margin before and after the data

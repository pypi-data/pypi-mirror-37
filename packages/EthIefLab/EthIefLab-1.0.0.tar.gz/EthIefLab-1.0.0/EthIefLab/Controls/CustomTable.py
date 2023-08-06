#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
30.05.2018

Description: The custom table allows to display parameter fields as well as results in a structured way by providing
a table class as well as cell classes that comprise attributes needed for the data representation.

"""

from .CustomFrame import CustomFrame
import EthIefLab.ObservableList as ObservableList
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar, Entry, Label, Frame, Checkbutton, NORMAL, DISABLED
import json
import os


class CustomTableCell(object):
    """
    The cell populates a custom table row. It has its own data type.
    """

    @property
    def value(self):
        """
        Gets value of the cell.
        :return: cell data
        """
        return self.variable.get()

    @value.setter
    def value(self, val):
        """
        Sets value of the cell.
        :param val: value to set the cell to
        """
        self.variable.set(val)

    _is_enabled = True

    @property
    def is_enabled(self):
        """
        Gets if the cell can be edited.
        :return: True or False
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, val):
        """
        Sets if the cell can be edited (cell will be grayed out if set to False)
        :param val: True or False
        """
        self._is_enabled = val

        if self.control_handle is not None:  # if a widget is using this cell set the appropriate state
            self.control_handle.config(state=NORMAL if self._is_enabled else DISABLED)

        for callback in self.enabled_changed:   # notify any subscribers about the change
            callback(self, self._is_enabled)

    def __init__(self, parent, cell_value=None, cell_type='float', name=None, unit=None, is_enabled=True):
        self._root = parent         # keep reference to the containing element
        self.cell_type = cell_type  # store the type of the cell (used for display of correct widget in the table)
        self.variable = None        # space for the tkinter variable
        self.enabled_changed = list()   # callback list to subscribe to the enabled changed event
        self.control_handle = None      # handle to the widget that uses this cell as data source
        self.name = name    # name of the cell (used to access it quickly via the CustomTableSource data structure)
        self.unit = unit    # the physical unit of this cell (if not None this will add the units in [] after the cell)
        self.is_enabled = is_enabled    # sets if the user can edit this cell

        # setup cell properties for various data types
        if cell_type == 'float' or cell_type == 'double':
            if cell_value is None: cell_value = 0
            self.variable = DoubleVar(parent, cell_value)
        elif cell_type == 'int':
            if cell_value is None: cell_value = 0
            self.variable = IntVar(parent, cell_value)
        elif cell_type == 'bool':
            if cell_value is None: cell_value = False
            self.variable = BooleanVar(parent, cell_value)
        elif cell_type == 'empty':
            self.variable = IntVar()
        else:
            self.variable = StringVar(parent, cell_value)


class CustomTableRow(object):
    """
    A row that makes up a custom table source.
    """

    def __iter__(self):
        """Iterator used for loop statements over all cells in this row."""
        for cell in self._cells:
            yield cell

    def __getitem__(self, index):
        """Returns the cell at the specified index (column)."""
        return self._cells[index]

    def __setitem__(self, index, value: CustomTableCell):
        """Sets the cell at the specified index (column)."""
        self._cells[index] = value

    def append(self, value: CustomTableCell):
        """
        Append cell to row.
        :param value: CustomCell to append to the row
        """
        self._cells.append(value)

    _cells = None

    @property
    def cells(self):
        """
        Gets the cells of this row.
        :return: collection of CustomCell objects
        """
        return self._cells

    @cells.setter
    def cells(self, value):
        """
        Sets the cells of this row.
        :param value: collection of CustomCell objects
        """
        self._cells = value

    def __init__(self, parent, *args):
        self._cells = list()    # initialize cells of this row
        self._root = parent     # store reference to containing object

        for cell in args:       # add cells
            self.append(cell)


class CustomTableSource(ObservableList):
    """
    Data source for CustomTable, containing rows. It has a special accessor such that custom_table_source[name] will
    look up the name of the cell in all rows of the table source and return it.
    This prohibits the need to search through each row manually.
    """

    def __getitem__(self, key):
        """Accessor either returns a specific row or a cell if a name was given as index."""
        if type(key) is str:    # search the rows for the cell with the given name
            for row in self:
                for cell in row:
                    if cell.name == key:
                        return cell
        else:
            return super(CustomTableSource, self).__getitem__(key)  # return row at given index


class CustomTable(CustomFrame):
    """
    This table allows for a flexible way of displaying different types of data.
    """

    _rows = None    # member that holds the row data source for the table

    @property
    def rows(self):
        """
        Gets the rows of the table.
        :return: collection of rows of the table
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        """
        Sets the rows of the table. This should be of the type CustomTableSource
        :param value: CustomTableSource
        """
        if self._rows is not None and self._rows is ObservableList:
            self._rows.item_added.remove(self.__row_added__)        # stop listening to changes of old source
            self._rows.item_removed.remove(self.__row_removed__)    # stop listening to changes of old source

        self._rows = value  # set new row source

        if self._rows is ObservableList:
            self._rows.item_added.remove(self.__row_added__)        # start listening to changes of new source
            self._rows.item_removed.remove(self.__row_removed__)    # start listening to changes of new source

            self._column_widths = list()        # initialize column width list
            if len(self._rows) > 0:
                self._column_widths = [None for i in range(len(self._rows))]

        self.__setup__()    # run setup to initialize all widgets that belong to the row data

    def get_col_width(self, col):
        """Gets the configured column width of the specified column."""
        return self._column_widths[col]

    def set_col_width(self, col, width):
        """
        Gets the configured column width of the specified column.
        :param col: Column index
        :param width: width of the column
        """
        self._column_widths[col] = width
        self.__setup__()    # re-run setup to account for the change

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # call the parent class's constructor
        self._root = parent  # keep reference to the ui parent
        self._column_widths = list()

    def __row_added__(self, row):
        self.__setup__()    # re-run setup to account for the change

    def __row_removed__(self, row):
        self.__setup__()    # re-run setup to account for the change

    def __setup__(self):
        self.clear()    # remove all existing widgets to clear the table

        if self._rows is None:  # do nothing if no row source is present
            return

        r = 0
        for row in self._rows:  # loop through all rows in the source
            c = 0
            for cell in row:    # loop through all cells in the current row source
                if c >= len(self._column_widths):
                    self._column_widths.append(None)    # add slot to column width list if it does not exist

                parent = self   # set parent to self if the widget has no unit label
                if cell.unit is not None:
                    '''if the cell has a unit label create a container frame where the unit label and the widget 
                    itself are positioned inside'''
                    cell_frame = self.add_widget(Frame(self), row=r, column=c)
                    parent = cell_frame

                # create widget according to cell type
                widget = None
                if cell.cell_type in ['float', 'int', 'double', 'text']:
                    widget = Entry(parent, textvariable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'label':
                    widget = Label(parent, textvariable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'bool':
                    widget = Checkbutton(parent, variable=cell.variable, width=self._column_widths[c])
                elif cell.cell_type == 'empty':
                    widget = Label(parent, width=self._column_widths[c])
                cell.control_handle = widget

                widget.config(state=NORMAL if cell.is_enabled else DISABLED)    # set widget enabled or disabled

                # add widget to table
                if cell.unit is not None:
                    self._children.append(widget)
                    widget.grid(row=0, column=0)
                    Label(parent, text='[{}]'.format(cell.unit)).grid(row=0, column=1)
                else:
                    self.add_widget(widget, row=r, column=c)
                c += 1
            r += 1

    def serialize(self, path):
        """
        Serializes data in table to json.
        :param path: path to save the serialized data to
        """
        if self.rows is None:
            return

        data = list()
        for row in self.rows:
            row_data = list()
            for cell in row:
                cell_data = dict()
                cell_data['cell_type'] = cell.cell_type
                cell_data['name'] = cell.name
                cell_data['unit'] = cell.unit
                cell_data['is_enabled'] = cell.is_enabled
                cell_data['value'] = cell.value
                row_data.append(cell_data)
            data.append(row_data)

        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def deserialize(self, path):
        """
        Deserializes the table data from a given file and loads it into the cells.
        :param path: path where the file with the serialized data is located
        """
        if self.rows is None or not os.path.isfile(path):
            return
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
            for row in range(len(data)):
                for col in range(len(data[row])):
                    cell = self.rows[row][col]
                    cell.value = data[row][col]['value']


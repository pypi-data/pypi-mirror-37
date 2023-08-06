#!/usr/bin/env python3

"""
IEF, ETH Zurich

Dominik Werner
24.04.2018

Description: The observable list can alert if mutations are made.

"""


class ObservableList(list):
    """
    This list can send notifications about changes.
    """

    def __init__(self, *args, **kwargs):
        super(ObservableList, self).__init__(*args, **kwargs)
        self.item_added = list()    # callback list for add events
        self.item_removed = list()  # callback list for remove events
        self.on_clear = list()      # callback list for clearing events

    def append(self, item):
        """
        Append item to the list. (Will also trigger notification)
        :param item: item to append to the list
        """
        super(ObservableList, self).append(item)

        for callback in self.item_added:    # execute all subscribed callback methods
            callback(item)

    def remove(self, item):
        """
        Remove item from the list. (Will also trigger notification)
        :param item: item to remove from the list
        """
        super(ObservableList, self).remove(item)

        for callback in self.item_removed:    # execute all subscribed callback methods
            callback(item)

    def clear(self):
        """
        Remove all items from list.
        """
        super(ObservableList, self).clear()

        for callback in self.on_clear:  # execute all subscribed callback methods
            callback()

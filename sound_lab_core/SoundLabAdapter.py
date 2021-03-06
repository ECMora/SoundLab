# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import QObject, pyqtSignal
import pyqtgraph as pg


class SoundLabAdapter(QObject):
    """
    Adapter-Factory Pattern Design implementation to bind
    support for segmentation classification and
    parameter measurement into the visual interface.
    """

    # region CONSTANTS

    # The color for the pen to create visual items
    # from segmentation or parameter measurement
    COLOR = pg.mkColor(QtGui.QColor(255, 20, 20, 255))

    # the width for the line on the visual items
    VISUAL_ITEM_LINE_WIDTH = 2

    # endregion

    # region SIGNALS

    # signal raised when a data has changed on the adapter settings
    # so the object returned by get_instance method has changed
    dataChanged = pyqtSignal()

    # endregion

    def __init__(self):
        QObject.__init__(self)

        # a name for the adapter
        self.name = ""

        # the db object mapper in the orm if any
        self.db_mapper = None

    def get_db_orm_mapper(self):
        """
        :return: The class that maps this adapter to it's
        sql db representation if any
        """
        return self.db_mapper

    def get_instance(self):
        """
        Gets a new get_instance of the corresponding adapted object .
        :return: An instance of the corresponding class
        """
        return None

    def state(self):
        """
        Memento pattern to save the current satate of the adapter
        :return: dict with object state
        """
        return {"name": self.name}

    def load_state(self, state):
        """
        Load an object state from the supplied one.
        :param state: dict with object state
        :return:
        """
        if not isinstance(state, dict):
            return

        self.name = state["name"] if "name" in state else self.name

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a Parameter Tree object to adapt each concrete object into the
        visual interface
        """
        return None

    def get_visual_items(self):
        """
        The list of the visual items to include in the visual widgets
        to visualize the Object instance (if any)
        :return:
        """
        return []

    def restore_settings(self, adapter_copy, signal):
        """
        Load into the settings of the current adapter the ones of the
        adapter supplied
        :type signal: AudioSignal
        :param adapter_copy: the adapter to load settings for
        :return:
        """
        # TODO must be examined to possible removed using load state implementation
        pass

# -*- coding: utf-8 -*-
from PyQt4 import QtGui


class VisualItemWrapper:
    """
    Represent a visual item to visualize inside a sound Lab Detected Element
    as representation of a measured parameter
    """

    # region CONSTANTS

    # the width of the line on the item
    ELEMENT_REGION_WIDTH = 3

    # endregion

    def __init__(self, color=None, tooltip=""):

        # the color for the pen to draw the item
        self.COLOR = QtGui.QColor(50, 50, 255, 255)

        if color is not None and isinstance(color, QtGui.QColor):
            self.COLOR = color

        self.tooltip = tooltip

    def set_data(self, signal, parameter, segment, data):
        """
        set the parameter measurement data to visualize it
        signal: Audio Signal in which the measurement was made.
        parameter: The parameter that measure the data. Its supplied to use the final locations
        in which the param was measured.
        segment: The segment on the signal in which the measurement was made.
        data: value of the measurement data.
        """
        pass

    def get_item(self):
        """
        returns the visual item to include on a visual widget
        """
        return None

    def clone(self):
        return self
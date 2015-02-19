# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from graphic_interface.segments.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import SpectralParameterVisualItem
import pyqtgraph as pg
import numpy as np


class AverageFreqVisualItem(SpectralParameterVisualItem):
    """
    """

    # region CONSTANTS
    # the color for the pen to draw the item
    COLOR = QtGui.QColor(50, 50, 255, 255)
    # endregion

    def __init__(self, color=None, tooltip=""):
        SpectralParameterVisualItem.__init__(self)
        self.indexFrom = 0
        self.indexTo = 0
        self.peak_freq_value = 0

        if color is not None and isinstance(color, QtGui.QColor):
            self.COLOR = color

        # a line for peak freq
        self.peak_freq_pos = np.array([[self.indexFrom,  self.peak_freq_value],
                                       [self.indexTo,  self.peak_freq_value]])

        self.peak_freq_adj = np.array([[0, 1]])
        self.peak_freq_region = pg.GraphItem()
        self.tooltip = tooltip

        self.peak_freq_region.setToolTip(self.tooltip)

    def get_item(self):
        return self.peak_freq_region

    def set_data(self, signal, segment, data):

        self.indexFrom = segment.indexFrom
        self.indexTo = segment.indexTo

        self.peak_freq_value = int(data)

        self.peak_freq_pos = np.array([[self.indexFrom,  self.peak_freq_value],
                                       [self.indexTo,  self.peak_freq_value]])
        self.peak_freq_region.setToolTip(self.tooltip + " " + str(int(data/1000.0)) + "(kHz)")

    def translate_time_freq_coords(self, translate_time_function=None, translate_freq_function=None):
        pos = np.zeros(4).reshape((2,2))

        if translate_time_function is not None:
            pos[0, 0] = translate_time_function(self.peak_freq_pos[0, 0])
            pos[1, 0] = translate_time_function(self.peak_freq_pos[1, 0])

        if translate_freq_function is not None:
            pos[0, 1] = translate_freq_function(self.peak_freq_pos[0, 1])
            pos[1, 1] = translate_freq_function(self.peak_freq_pos[1, 1])

        options = dict(size=1, symbol='d', pxMode=False, pen=(pg.mkPen(self.COLOR, width=5)))
        self.peak_freq_region.setData(pos=pos, adj=self.peak_freq_adj, **options)

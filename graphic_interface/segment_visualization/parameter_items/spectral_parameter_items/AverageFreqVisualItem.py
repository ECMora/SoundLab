# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import \
    SpectralVisualItemWrapper
import pyqtgraph as pg
import numpy as np


class AverageFreqVisualItem(SpectralVisualItemWrapper):

    def __init__(self, color=None, tooltip=""):
        """
        :param color: the color for the lines
        :param tooltip: an optional tooltip to show
        :return:
        """
        SpectralVisualItemWrapper.__init__(self, color=color, tooltip=tooltip)
        # time limits
        self.indexFrom = 0
        self.indexTo = 0


        # the freq value
        self.peak_freq_value = 0

        # a line for peak freq
        self.peak_freq_pos = np.array([[self.indexFrom,  self.peak_freq_value],
                                       [self.indexTo,  self.peak_freq_value]])

        self.peak_freq_adj = np.array([[0, 1]])
        self.peak_freq_region = pg.GraphItem()

        self.peak_freq_region.setToolTip(self.tooltip)

    def get_item(self):
        return self.peak_freq_region

    def clone(self):
        return AverageFreqVisualItem(self.COLOR, self.tooltip)

    def set_data(self, signal, parameter, segment, data_kHz):

        self.peak_freq_value = int(data_kHz*1000)

        param_name = parameter.getName()

        # update positions
        self.peak_freq_pos = np.array([[parameter.time_location.time_start_index,  self.peak_freq_value],
                                       [parameter.time_location.time_end_index,  self.peak_freq_value]])

        self.peak_freq_region.setToolTip(self.tooltip + " " + str(data_kHz) + "(kHz)" + param_name)

    def translate_time_freq_coords(self, translate_time_function=None, translate_freq_function=None):
        pos = np.zeros(4).reshape((2, 2))

        if translate_time_function is not None:
            pos[0, 0] = translate_time_function(self.peak_freq_pos[0, 0])
            pos[1, 0] = translate_time_function(self.peak_freq_pos[1, 0])

        if translate_freq_function is not None:
            pos[0, 1] = translate_freq_function(self.peak_freq_pos[0, 1])
            pos[1, 1] = translate_freq_function(self.peak_freq_pos[1, 1])

        options = dict(size=20, symbol='+', pxMode=False, pen=(pg.mkPen(self.COLOR, width=self.ELEMENT_REGION_WIDTH)))
        self.peak_freq_region.setData(pos=pos,  **options) #adj=self.peak_freq_adj,

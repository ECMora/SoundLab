# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeVisualItemWrapper
import pyqtgraph as pg


class PeakToPeakVisualItem(TimeVisualItemWrapper):

    def __init__(self, color=None, tooltip=""):
        TimeVisualItemWrapper.__init__(self, color=color, tooltip=tooltip)

    def clone(self):
        return PeakToPeakVisualItem(self.COLOR, self.tooltip)


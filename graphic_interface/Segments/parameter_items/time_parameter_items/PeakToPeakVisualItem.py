# -*- coding: utf-8 -*-
from graphic_interface.segments.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeParameterVisualItem
import pyqtgraph as pg


class PeakToPeakVisualItem(TimeParameterVisualItem):
    """
    Represents the visual parameter items for time measurements (oscilogram)
    """

    def __init__(self):
        TimeParameterVisualItem.__init__(self)

        # test label
        # the visible text for number




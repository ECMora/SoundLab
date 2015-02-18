# -*- coding: utf-8 -*-
from graphic_interface.segments.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeParameterVisualItem


class PeakToPeakVisualItem(TimeParameterVisualItem):
    """
    Represents the visual parameter items for time measurements (oscilogram)
    """

    def __init__(self, index_from, index_to):
        TimeParameterVisualItem.__init__(self)

        # the time limits of the parameter item
        self.indexFrom = index_from
        self.indexTo = index_to



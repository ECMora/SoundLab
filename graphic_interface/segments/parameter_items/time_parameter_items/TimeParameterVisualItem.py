# -*- coding: utf-8 -*-
from graphic_interface.segments.parameter_items.ParameterVisualItem import ParameterVisualItem


class TimeParameterVisualItem(ParameterVisualItem):
    """
    Represents the visual parameter items for time measurements (oscilogram)
    """

    def __init__(self, index_from=0, index_to=0):
        ParameterVisualItem.__init__(self)

        # the time limits of the parameter item
        self.indexFrom = index_from
        self.indexTo = index_to



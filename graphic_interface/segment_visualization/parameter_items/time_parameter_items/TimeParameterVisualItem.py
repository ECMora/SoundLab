# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.VisualItemWrapper import VisualItemWrapper


class TimeVisualItemWrapper(VisualItemWrapper):
    """
    Represents the visual parameter items for time parameters (oscilogram)
    """

    def __init__(self, index_from=0, index_to=0):
        VisualItemWrapper.__init__(self)

        # the time limits of the parameter item
        self.indexFrom = index_from
        self.indexTo = index_to



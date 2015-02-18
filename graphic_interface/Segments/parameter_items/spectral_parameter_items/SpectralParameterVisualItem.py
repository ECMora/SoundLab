# -*- coding: utf-8 -*-
from graphic_interface.segments.parameter_items.ParameterVisualItem import ParameterVisualItem


class SpectralParameterVisualItem(ParameterVisualItem):
    """
    Represents the visual parameter items for time measurements (oscilogram)
    """

    def __init__(self, index_from, index_to):
        ParameterVisualItem.__init__(self)

        # the time limits of the parameter item
        self.indexFrom = index_from
        self.indexTo = index_to

    def translate_time_freq_coords(self, translate_time_function=None, translate_freq_function=None):
        """

        :return:
        """
        pass
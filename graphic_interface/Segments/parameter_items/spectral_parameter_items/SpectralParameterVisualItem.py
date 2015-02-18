# -*- coding: utf-8 -*-
from graphic_interface.segments.parameter_items.ParameterVisualItem import ParameterVisualItem


class SpectralParameterVisualItem(ParameterVisualItem):
    """
    Represents the visual parameter items for time measurements (oscilogram)
    """

    def __init__(self):
        ParameterVisualItem.__init__(self)

    def translate_time_freq_coords(self, translate_time_function=None, translate_freq_function=None):
        """

        :return:
        """
        pass
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
        Translate the coordinates system of the item when a change is made on the spectrogram matrix.

        :param translate_time_function: the callable to translate the time axis. (x_time) => new_x_time
        :param translate_freq_function: the callable to translate the freq axis. (x_freq) => new_x_freq
        :return:
        """
        pass
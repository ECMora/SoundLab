#  -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.OscilogramElement import OscilogramElement
from graphic_interface.segment_visualization.SpectrogramElement import SpectrogramElement
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import \
    SpectralVisualItemWrapper
from graphic_interface.segment_visualization.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeVisualItemWrapper


class DetectedSoundLabElement:
    """
    Class that represents a detected signal element.
    Contains the visual elements of time and spectral domains
    """

    def __init__(self, signal, index_from, index_to, number=0, signal_callback=None):
        self.signal = signal

        # the time domain visual element
        self._time_element = OscilogramElement(signal, index_from, index_to, number)

        # the spectral domain visual element
        self._spectral_element = SpectrogramElement(signal, index_from, index_to, number)

        self.set_element_clicked_callback(signal_callback)

    def set_bounds(self, index_from, index_to):
        self.time_element.set_bounds(index_from, index_to)
        self.spectral_element.set_bounds(index_from, index_to)

    def set_element_clicked_callback(self, callback):
        """

        :param callback:
        :return:
        """
        # callback to execute when the element is clicked. Signals are not used for efficiency
        self._time_element.set_element_clicked_callback(callback)
        self._spectral_element.set_element_clicked_callback(callback)

    # region Properties

    @property
    def number(self):
        return self._time_element.number

    @property
    def visible(self):
        """
        :return: the visibility of the detected element on visual widgets
        """
        return self.time_element.visible or self.spectral_element.visible

    @visible.setter
    def visible(self, value):
        # set the visibility of the two domain representations
        self.time_element.visible = value
        self.spectral_element.visible = value

    def set_signal(self, value):
        # set the visibility of the two domain representations
        self.time_element.signal = value
        self.spectral_element.signal = value

    @property
    def indexFrom(self):
        return self.time_element.indexFrom

    @property
    def indexTo(self):
        return self.time_element.indexTo


    @property
    def spectral_element(self):
        return self._spectral_element

    @property
    def time_element(self):
        return self._time_element

    # endregion

    def add_visual_item(self, parameter_item):
        """
        Add a parameter item into the visual element representation
        :param parameter_item: A measured parameter visualization item
        :return:
        """
        if isinstance(parameter_item, TimeVisualItemWrapper):
            self.time_element.add_parameter_item(parameter_item)

        elif isinstance(parameter_item, SpectralVisualItemWrapper):
            self.spectral_element.add_parameter_item(parameter_item)

    def setNumber(self, n):
        """
        Change the number of the detected element on the system.
        Must be updated the labels and numbers of the visual items
        :param n: The new number of the element
        :return:
        """
        self.time_element.setNumber(n)
        self.spectral_element.setNumber(n)
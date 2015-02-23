#  -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, QObject
from graphic_interface.segments.OscilogramElement import OscilogramElement
from graphic_interface.segments.SpectrogramElement import SpectrogramElement
from graphic_interface.segments.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import \
    SpectralParameterVisualItem
from graphic_interface.segments.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeParameterVisualItem


class DetectedSoundLabElement(QObject):
    """
    Class that represents a detected signal element.
    Contains the visual elements of time and spectral domains
    """

    # region SIGNALS
    # called when the element is clicked
    # raise the index of the element (number)
    elementClicked = pyqtSignal(int)
    # endregion

    def __init__(self, signal, index_from, index_to, number=0):
        QObject.__init__(self)
        self.signal = signal

        # the time domain visual element
        self._time_element = OscilogramElement(signal, index_from, index_to, number)
        self._time_element.elementClicked.connect(lambda i: self.elementClicked.emit(i))

        # the spectral domain visual element
        self._spectral_element = SpectrogramElement(signal, index_from, index_to, number)
        self._spectral_element.elementClicked.connect(lambda i: self.elementClicked.emit(i))

    # region Properties

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

    def add_parameter_item(self, parameter_item):
        """
        Add a parameter item into the visual element representation
        :param parameter_item: A measured parameter visualization item
        :return:
        """
        if isinstance(parameter_item, TimeParameterVisualItem):
            self.time_element.add_parameter_item(parameter_item)

        elif isinstance(parameter_item, SpectralParameterVisualItem):
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
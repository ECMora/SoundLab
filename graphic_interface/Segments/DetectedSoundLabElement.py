#  -*- coding: utf-8 -*-
from VisualElement import VisualElement
from graphic_interface.segments.OscilogramElement import OscilogramElement
from graphic_interface.segments.SpectrogramElement import SpectrogramElement


class DetectedSoundLabElement(VisualElement):
    """

    """

    def __init__(self, signal, index_from, index_to, number=0):
        self._time_element = OscilogramElement(signal, index_from, index_to, number)
        self._time_element.elementClicked.connect(lambda i: self.elementClicked.emit(i))

        self._spectral_element = SpectrogramElement(signal, index_from, index_to, number)
        self._spectral_element.elementClicked.connect(lambda i: self.elementClicked.emit(i))

        # last to override the visible variable
        VisualElement.__init__(self, number)

    # region Properties

    @property
    def visible(self):
        return self.time_element.visible

    @visible.setter
    def visible(self, value):
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

    def setNumber(self, n):
        self.time_element.setNumber(n)
        self.spectral_element.setNumber(n)
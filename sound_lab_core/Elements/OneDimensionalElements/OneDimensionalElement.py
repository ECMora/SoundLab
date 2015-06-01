#  -*- coding: utf-8 -*-
from sound_lab_core.Elements.Element import Element


class OneDimensionalElement(Element):
    """
    Element defined in a one-dimensional acoustic processing over a signal
    """

    def __init__(self, signal, indexFrom, indexTo):
        Element.__init__(self, signal)
        self.indexFrom = indexFrom
        self.indexTo = indexTo

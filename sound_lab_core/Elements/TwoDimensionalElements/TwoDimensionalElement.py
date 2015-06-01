# -*- coding: utf-8 -*-
from sound_lab_core.Elements.Element import Element


class TwoDimensionalElement(Element):
    """
    """

    def __init__(self, signal, matrix):
        Element.__init__(self, signal)
        self.matrix = matrix


# -*- coding: utf-8 -*-
from sound_lab_core.Elements.Element import Element


class TwoDimensionalElement(Element):
    """
    In an acoustic processing one_dim_transform of 2 dimensional as
    spectrogram an element is a 2 dimensional region
    of local maximum in the rectangular matrix of specgram
    """

    def __init__(self, signal, matrix):
        Element.__init__(self, signal)
        self.matrix = matrix


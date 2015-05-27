#  -*- coding: utf-8 -*-
from numpy import *

from sound_lab_core.Segmentation.ElementsDetector import ElementsDetector
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement


class OneDimensionalElementsDetector(ElementsDetector):
    """
    A one dimensional elements detector is based in compute
    one dimensional areas (intervals [start, end] ) over an acoustic processing of one dimension.
    """

    def __init__(self, signal, min_size_ms=1, merge_factor=5, one_dimensional_class=OneDimensionalElement):
        """
        :param signal: The signal in which would be detected the elements
        :param min_size_ms: The min size of a detected element is ms. Parameter to filter detected elements.
        :param merge_factor: The factor of separation between consecutive elements that would be merged
         into one. Parameter to filter detected elements.
        :param one_dimensional_class: one_dimensional_class: The dependency injection for the
        one dimensional element to use
        :return:
        """
        ElementsDetector.__init__(self, signal)

        # post detection filter variables
        self._merge_factor = merge_factor
        self._min_size = min_size_ms

        self.one_dimensional_class = one_dimensional_class

    # region Properties

    @property
    def merge_factor(self):
        return self._merge_factor

    @merge_factor.setter
    def merge_factor(self, value):
        self._merge_factor = value

    @property
    def min_size(self):
        return self._min_size

    @min_size.setter
    def min_size(self, value):
        self._min_size = value

    # endregion

    def get_one_dimensional_class(self):
        """
        The instance of the detected one dimensional elements to return
        :return:
        """
        return self.one_dimensional_class

    def detect(self, indexFrom=0, indexTo=-1):
        """
        :param indexFrom:
        :param indexTo:
        :return:
        """
        return self.elements

    def merge_intervals(self, elements_array):
        """
        Merge into one interval two elements with no more than  distance factor distance between them
        """
        if elements_array is None or len(elements_array) == 0:
            return []

        if self.merge_factor <= 0:
            return elements_array

        result = [elements_array[0]]

        for t in elements_array[1:]:
            while len(result) > 0:
                current = result.pop()
                if (t[0] - current[1]) * 100.0 / (t[1] - current[0]) < self.merge_factor:
                    t = (current[0], t[1])
                else:
                    result.append(current)
                    break
            result.append(t)

        return result



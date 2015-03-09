#  -*- coding: utf-8 -*-
from numpy import *
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement
from sound_lab_core.Segmentation.Detectors.ElementsDetector import ElementsDetector


class OneDimensionalElementsDetector(ElementsDetector):

    def __init__(self, signal, one_dimensional_class=OneDimensionalElement):
        """
        :param signal: The signal in wchich would be detected the elements
        :param one_dimensional_class: The dependency injection for the
        one dimensional element to use
        :return:
        """
        ElementsDetector.__init__(self, signal)
        self.one_dimensional_class = one_dimensional_class

    def get_one_dimensional_class(self):
        """
        The instance of the detected one dimensional elements
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

    def merge_intervals(self, elements_array, distance_factor=50):
        """
        Merge into one interval two elements with no more than  distance factor distance between them
        """
        if elements_array is None or len(elements_array) == 0:
            return []

        result = [elements_array[0]]

        for t in elements_array[1:]:
            while len(result) > 0:
                current = result.pop()
                if (t[0] - current[1]) * 100.0 / (t[1] - current[0]) < distance_factor:
                    t = (current[0], t[1])
                else:
                    result.append(current)
                    break
            result.append(t)

        return result

    def local_max(self, data):
        """
        Identify the local  (positives or not) max that are above threshold
        :param data:  Array of int with the signal data information
        :return:
        """
        data = abs(array(data))

        indexes = [i for i in xrange(1, data.size - 1) if ((data[i] > data[i - 1]) and (data[i] > data[i + 1])) or
                                                          (data[i] == data[i - 1] == data[i + 1])]
        return array(indexes), data[indexes]

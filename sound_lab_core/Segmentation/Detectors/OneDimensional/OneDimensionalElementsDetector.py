#  -*- coding: utf-8 -*-
from numpy import *
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement
from sound_lab_core.Segmentation.Detectors.ElementsDetector import ElementsDetector


class OneDimensionalElementsDetector(ElementsDetector):

    def __init__(self, signal):
        ElementsDetector.__init__(self, signal)

    def get_one_dimensional_class(self):
        """
        The instance of the detected one dimensional elements
        :return:
        """
        return OneDimensionalElement

    def detect(self, indexFrom=0, indexTo=-1):
        """
        :param indexFrom:
        :param indexTo:
        :return:
        """
        pass

    def merge_intervals(self, elements_array, distance_factor=50):
        """
        Merge into one interval two elements with no more than  distance factor distance between them
        """
        if elements_array is None or len(elements_array) == 0:
            return []

        change = True
        while change:
            change = False
            current = elements_array[0]
            result = []

            for t in elements_array[1:]:
                if (t[0] - current[1]) * 100.0 / (t[1] - current[0]) < distance_factor:
                    current = (current[0], t[1])
                    change = True
                else:
                    result.append(current)
                    current = t

            result.append(current)
            elements_array = result

        return elements_array

    def localMax(self, data, threshold=0, positives=None):
        """
        Identify the local  (positives or not) maxThresholdLabel that are above threshold
        :param data:  Array of int with the signal data information
        :param threshold:
        :param positives: Searh for local max positives
        :return:
        """
        indexes = []
        values = []
        data = array(data)

        if positives is not None and positives:
            data = where(data >= threshold, data, 0)
        elif positives is not None:
            data = where(data < -threshold, data, 0)

        data = abs(data)

        for i in range(1,data.size-1):
            if (data[i] > data[i - 1] and data[i] > data[i + 1]) or (data[i] == data[i - 1] == data[i + 1]):
                indexes.append(i)
                values.append(data[i])

        return array(indexes), array(values)

#  -*- coding: utf-8 -*-
from numpy import *
from sound_lab_core.Segmentation.Detectors.ElementsDetector import ElementsDetector


class OneDimensionalElementsDetector(ElementsDetector):

    def __init__(self, signal):
        ElementsDetector.__init__(self, signal)

    @property
    def one_dimensional_element(self):
        """
        The instance of the detected one dimensional elements
        :return:
        """
        pass

    def detect(self, indexFrom=0, indexTo=-1):
        """
        :param indexFrom:
        :param indexTo:
        :return:
        """
        pass

    def mergeIntervals(self, elements_array, distancefactor=50):
        """
        Merge into one interval two elements with no more than  distance factor distance between them
        """
        result = []
        if elements_array is None or len(elements_array) == 0:
            return []

        current = elements_array[0]
        for tuple in elements_array[1:]:
            if (tuple[0] - current[1]) * 100.0 / (tuple[1] - current[0]) < distancefactor:
                current = (current[0], tuple[1])

            else:
                result.append(current)
                current = tuple
        result.append(current)
        return result

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

        return array(indexes),array(values)

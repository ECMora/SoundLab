#  -*- coding: utf-8 -*-
from numpy import *

from sound_lab_core.Segmentation.ElementsDetector import ElementsDetector
from utils.Utils import fromdB
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement


class OneDimensionalElementsDetector(ElementsDetector):
    """
    A one dimensional elements detector is based in compute
    one dimensional areas (intervals [start, end] ) over an acoustic processing of one dimension.
    """

    def __init__(self, signal, threshold_db=-40, threshold2_db=-40, threshold3_db=-40,
                 min_size_ms=1, merge_factor=5, one_dimensional_class=OneDimensionalElement):
        """
        :param signal: The signal in which would be detected the elements
        :param threshold_db: The threshold to detect elements on the one dim acoustic processing
        :param threshold2_db: The threshold to detect elements on the one dim acoustic processing.
        (start of the element). if 0 then would be ignored
        :param threshold3_db: The threshold to detect elements on the one dim acoustic processing.
        (end of the element). if 0 then would be ignored
        :param min_size_ms: The min size of a detected element is ms. Parameter to filter detected elements.
        :param merge_factor: The factor of separation between consecutive elements that would be merged
         into one. Parameter to filter detected elements.
        :param one_dimensional_class: one_dimensional_class: The dependency injection for the
        one dimensional element to use
        :return:
        """
        ElementsDetector.__init__(self, signal)

        # variables for detection
        self._threshold = threshold_db
        self._threshold2 = threshold2_db
        self._threshold3 = threshold3_db

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

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    @property
    def threshold2(self):
        return self._threshold2

    @threshold2.setter
    def threshold2(self, value):
        self._threshold2 = value

    @property
    def threshold3(self):
        return self._threshold3

    @threshold3.setter
    def threshold3(self, value):
        self._threshold3 = value

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

    def detect_elements_start_end_thresholds(self, elems, acoustic_processing):
        """
        Detect the start and end of the detected elements using three thresholds.
        :param elems: List of tuples (start, end) of detected elements with one threshold
        over the acoustic processing supplied.
        :param acoustic_processing:
        :return:
        """
        if self.threshold2 < 0 or self.threshold3 < 0:
            # use both thresholds start and end
            result = []
            for element in elems:
                max_amplitude = max(acoustic_processing[element[0]: element[1]])

                start_threshold_db = fromdB(self.threshold2, 0, max_amplitude)
                end_threshold_db = fromdB(self.threshold3, 0, max_amplitude)

                start_index, end_index = element
                # find start
                while acoustic_processing[start_index] > start_threshold_db and start_index > 0:
                    start_index -= 1

                # find end
                while acoustic_processing[end_index] > end_threshold_db and end_index < len(acoustic_processing):
                    end_index += 1

                result.append((start_index, end_index))

            return result

        return elems

    def filter_by_min_size(self, elements):
        return elements

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

    def local_max(self, data):
        """
        Identify the local  (positives or not) max that are above threshold
        :param data:  Array of int with the signal data information
        :return:
        """
        data = abs(array(data))

        indexes = [i for i in xrange(1, data.size - 1) if (data[i - 1] < data[i] > data[i + 1]) or
                                                          (data[i] == data[i - 1] == data[i + 1])]

        return array(indexes), data[indexes]

from math import sqrt
import matplotlib.mlab as mlab
import numpy as np
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from Utils.Utils import fromdB


class IntervalDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, threshold_db=-40, min_size_ms=1, merge_factor=5):
        OneDimensionalElementsDetector.__init__(self, signal)

        self._threshold = threshold_db
        self._merge_factor = merge_factor
        self._min_size = min_size_ms

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

    # endregion

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        threshold = fromdB(self.threshold, 0, self.signal.maximumValue)

        min_size = int(self.min_size * self.signal.samplingRate / 1000.0)

        elems = self.detect_elements(self.signal.data[indexFrom:indexTo], threshold, min_size, self.merge_factor)

        self.detectionProgressChanged.emit(90)

        self.elements = [None for _ in elems]
        one_dim_class = self.get_one_dimensional_class()

        for i, c in enumerate(elems):
            self.elements[i] = one_dim_class(self.signal, c[0], c[1])

        self.detectionProgressChanged.emit(100)

        return self.elements

    def interval_detector(self, data, threshold, minSize, merge_factor, function, comparer_greater_threshold=True):
        """
        if comparer_greater_threshold then the intervals > threshold else intervals < threshold would be acepted
        """

        minSize = int(minSize)
        if minSize == 0:
            minSize = len(data) / 1000

        self.detectionProgressChanged.emit(5)

        f_interval = lambda ind: function(data[ind - minSize / 2:ind + minSize / 2])

        detected = np.array([f_interval(i) for i in np.arange(minSize / 2, data.size, minSize / 2)])

        self.detectionProgressChanged.emit(50)

        if comparer_greater_threshold:
            detected = mlab.contiguous_regions(detected > threshold)
        else:
            detected = mlab.contiguous_regions(detected < threshold)

        self.detectionProgressChanged.emit(70)

        detected = [((x[0]) * minSize / 2, (x[1]) * minSize / 2) for x in detected if x[1] > 1 + x[0]]

        if merge_factor > 0:
            detected = self.mergeIntervals(detected, merge_factor)

        return detected

    def detect_elements(self, data, threshold, minSize, merge_factor):
        def function(d):
            ind, vals = self.localMax(d)
            x = 0
            if len(vals) > 0:
                vals = np.array(vals, dtype=long)
                x = sqrt(sum(vals ** 2) / vals.size)
            return x

        return self.interval_detector(data, threshold, minSize, merge_factor, function)


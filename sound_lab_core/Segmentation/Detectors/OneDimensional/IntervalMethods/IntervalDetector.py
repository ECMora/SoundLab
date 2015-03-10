from math import sqrt
import matplotlib.mlab as mlab
import numpy as np
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from utils.Utils import fromdB


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

        threshold = fromdB(self.threshold, 0, max(self.signal.data))

        min_size = int(self.min_size * self.signal.samplingRate / 1000.0)

        elems = self.detect_elements(self.signal.data[indexFrom:indexTo], threshold, min_size, self.merge_factor)

        self.detectionProgressChanged.emit(90)

        one_dim_class = self.get_one_dimensional_class()
        self.elements = [one_dim_class(self.signal, c[0], c[1]) for c in elems]

        self.detectionProgressChanged.emit(100)

        return self.elements

    def interval_detector(self, data, threshold, min_size, merge_factor, function, comparer_greater_threshold=True):
        """
        if comparer_greater_threshold then the intervals > threshold else intervals < threshold would be acepted
        """

        min_size = int(min_size)
        if min_size == 0:
            min_size = self.signal.samplingRate / 1000

        self.detectionProgressChanged.emit(5)

        arr_size = ((data.size * 2) / min_size)

        k = min_size / 2
        detected = np.array([0 if i == 0 else function(data[(i - 1) * k: i * k]) for i in xrange(arr_size)])

        self.detectionProgressChanged.emit(50)

        detected = mlab.contiguous_regions(detected > threshold if comparer_greater_threshold else detected < threshold)

        self.detectionProgressChanged.emit(80)

        detected = [((x[0] - 1) * min_size / 2, (x[1]) * min_size / 2) for x in detected if x[1] > 1 + x[0]]

        if merge_factor > 0:
            detected = self.merge_intervals(detected, merge_factor)

        return detected

    def function(self, d):
        return 0

    def detect_elements(self, data, threshold, minSize, merge_factor):
        return self.interval_detector(data, threshold, minSize, merge_factor, self.function)


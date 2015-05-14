import numpy as np

from sound_lab_core.Segmentation.OneDimensional.IntervalMethods.IntervalDetector import IntervalDetector
from utils.Utils import fromdB


class IntervalMaxDetector(IntervalDetector):

    def __init__(self, signal, threshold_db=-40, threshold2_db=0, threshold3_db=0, min_size_ms=1, merge_factor=5):
        IntervalDetector.__init__(self, signal, threshold_db, threshold2_db, threshold3_db,
                                  min_size_ms, merge_factor)

    def get_threshold_level(self, data):
        return fromdB(self.threshold, 0, max(self.signal.data))

    def interval_function(self, data, step, total):
        IntervalDetector.interval_function(self, data, step, total)
        return np.max(np.abs(data))

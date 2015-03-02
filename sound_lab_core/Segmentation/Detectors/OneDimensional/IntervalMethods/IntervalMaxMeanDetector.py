from math import sqrt
import numpy as np
from sound_lab_core.Segmentation.Detectors.OneDimensional.IntervalMethods.IntervalDetector import IntervalDetector


class IntervalMaxMeanDetector(IntervalDetector):

    def __init__(self, signal, threshold_db=-40, min_size_ms=1, merge_factor=5):
        IntervalDetector.__init__(self, signal,threshold_db, min_size_ms, merge_factor)

    def function(self, d):
        return self.localMax(d)[1].mean()

    def detect_elements(self, data, threshold, minSize, merge_factor):
        return self.interval_detector(data, threshold, minSize, merge_factor, self.function)

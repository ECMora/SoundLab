from sound_lab_core.Segmentation.Detectors.OneDimensional.IntervalMethods.IntervalDetector import IntervalDetector


class IntervalMaxMeanDetector(IntervalDetector):

    def __init__(self, signal, threshold_db=-40, min_size_ms=1, merge_factor=5):
        IntervalDetector.__init__(self, signal,threshold_db, min_size_ms, merge_factor)

    def function(self, data, step, total):
        IntervalDetector.function(self, data, step, total)

        return self.local_max(data)[1].mean()
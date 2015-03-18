from sound_lab_core.Segmentation.Detectors.OneDimensional.IntervalMethods.IntervalDetector import IntervalDetector


class IntervalRmsDetector(IntervalDetector):

    def __init__(self, signal, threshold_db=-40, threshold2_db=0, threshold3_db=0, min_size_ms=1, merge_factor=5):
        IntervalDetector.__init__(self, signal, threshold_db, threshold2_db, threshold3_db,
                                  min_size_ms, merge_factor)

    def interval_function(self, data, step, total):
        IntervalDetector.interval_function(self, data, step, total)

        _, values = self.local_max(data)

        if len(values) == 0:
            return 0

        return (values ** 2).sum() ** 0.5 / values.size
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalEnvelope import IntervalEnvelope
from utils.Utils import fromdB


class IntervalMaxMeanEnvelope(IntervalEnvelope):

    def __init__(self, signal=None, threshold_db=-40, min_size=40):
        IntervalEnvelope.__init__(self, threshold_db, min_size)
        self.max_value = 0

    def get_threshold_level(self, data):
        return fromdB(self.threshold, 0, self.max_value)

    def interval_function(self, data, step, total):
        IntervalEnvelope.interval_function(self, data, step, total)

        # update max value
        value = self.local_max(data)[1].mean()
        self.max_value = max(self.max_value, value)

        return value

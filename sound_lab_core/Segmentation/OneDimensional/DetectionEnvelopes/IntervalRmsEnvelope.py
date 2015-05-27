from numpy import sqrt, mean, square

from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalEnvelope import IntervalEnvelope


class IntervalRmsEnvelope(IntervalEnvelope):

    def __init__(self, signal=None, threshold_db=-40, min_size=40):
        IntervalEnvelope.__init__(self, threshold_db, min_size)

    def interval_function(self, data, step, total):
        IntervalEnvelope.interval_function(self, data, step, total)
        return sqrt(mean(square(data.astype("int32"))))

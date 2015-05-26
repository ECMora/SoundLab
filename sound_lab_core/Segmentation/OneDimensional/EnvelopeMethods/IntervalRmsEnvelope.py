from numpy import sqrt, mean, square

from sound_lab_core.Segmentation.OneDimensional.EnvelopeMethods.IntervalEnvelope import IntervalEnvelope


class IntervalRmsEnvelope(IntervalEnvelope):

    def __init__(self, threshold_db=-40):
        IntervalEnvelope.__init__(self, threshold_db)

    def interval_function(self, data, step, total):
        IntervalEnvelope.interval_function(self, data, step, total)
        return sqrt(mean(square(data.astype("int32"))))

from sound_lab_core.Segmentation.OneDimensional.EnvelopeMethods.IntervalEnvelope import IntervalEnvelope


class IntervalMaxMeanEnvelope(IntervalEnvelope):

    def __init__(self, threshold_db=-40):
        IntervalEnvelope.__init__(self, threshold_db)

    def interval_function(self, data, step, total):
        IntervalEnvelope.interval_function(self, data, step, total)

        return self.local_max(data)[1].mean()

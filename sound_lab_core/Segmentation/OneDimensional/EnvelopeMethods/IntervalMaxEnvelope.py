import numpy as np

from sound_lab_core.Segmentation.OneDimensional.EnvelopeMethods.IntervalEnvelope import IntervalEnvelope
from utils.Utils import fromdB


class IntervalMaxEnvelope(IntervalEnvelope):

    def __init__(self, signal=None, threshold_db=-40):
        IntervalEnvelope.__init__(self, threshold_db)

        self.max_value = 2**16 if signal is None else max(signal.data)

    def get_threshold_level(self, data):
        return fromdB(self.threshold, 0, self.max_value)

    def interval_function(self, data, step, total):
        IntervalEnvelope.interval_function(self, data, step, total)
        return np.max(np.abs(data))
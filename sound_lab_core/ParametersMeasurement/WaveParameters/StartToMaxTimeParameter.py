# -*- coding: utf-8 -*-
import numpy as np
from sound_lab_core.ParametersMeasurement.TimeParameters.TimeParameter import TimeParameter


class StartToMaxTimeParameter(TimeParameter):
    """
    Class that measure the start to max time paramter on a segment
    """

    def __init__(self, decimal_places=4):
        TimeParameter.__init__(self, decimal_places=decimal_places)
        self.name = "StartToMax(s)"

    def measure(self, segment):
        return round(np.argmax(segment.signal.data[segment.indexFrom:segment.indexTo])
                     * 1.0 / segment.signal.samplingRate, self.decimal_places)
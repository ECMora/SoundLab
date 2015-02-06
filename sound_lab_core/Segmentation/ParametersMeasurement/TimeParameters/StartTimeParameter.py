# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.ParametersMeasurement.Parameter import SegmentParameterMeasurer


class StartTimeParameter(SegmentParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        SegmentParameterMeasurer.__init__(self)
        self.name = "Start(s)"

    def measure(self, segment):
        return 0
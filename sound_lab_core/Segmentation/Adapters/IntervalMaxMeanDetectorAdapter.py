# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.OneDimensional.IntervalMethods.IntervalMaxMeanDetector import IntervalMaxMeanDetector
from sound_lab_core.Segmentation.Adapters.IntervalDetectorAdapter import IntervalDetectorAdapter


class IntervalMaxMeanDetectorAdapter(IntervalDetectorAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        IntervalDetectorAdapter.__init__(self)

    def get_instance(self, signal):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        self.update_instance_variables()
        self.signal_max_value = max(signal.data)

        return IntervalMaxMeanDetector(signal, self.threshold_dB, self.threshold2_dB,
                                       self.threshold3_dB, self.min_size_ms, self.merge_factor)

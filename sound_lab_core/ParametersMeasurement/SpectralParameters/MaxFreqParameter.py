# -*- coding: utf-8 -*-
import numpy as np

from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class MaxFreqParameter(FreqParameter):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2, time_measurement_location=None):
        FreqParameter.__init__(self, threshold, total, decimal_places=decimal_places,
                               time_measurement_location=time_measurement_location)
        self.name = "MaxFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        value = np.amax(Pxx) * np.power(10,self.threshold/10.0)

        if self.total:
            max_freq_index = np.argwhere(Pxx >= value).max()
        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[:peak_index] = False
            max_freq_index = np.argwhere(below).min() - 1
        return round((freqs[max_freq_index] - freqs[max_freq_index] % 10)/1000.0, self.decimal_places)

    def get_visual_items(self):
        if isinstance(self.time_location, MeanMeasurementLocation):
            return [AverageFreqVisualItem(tooltip=self.tr(u"Max Freq") + u" at " + unicode(self.threshold) + u" dB->")]
        return []
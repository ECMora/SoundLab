# -*- coding: utf-8 -*-
import numpy as np

from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class MinFreqParameter(FreqParameter):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2,
                 time_measurement_location=None):
        FreqParameter.__init__(self,threshold, total, decimal_places=decimal_places,
                               time_measurement_location=time_measurement_location)
        self.name = "MinFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        min_freq_limit_index, max_freq_limit_index = self.spectral_location.get_freq_limits(freqs)

        Pxx = Pxx[min_freq_limit_index:max_freq_limit_index]

        if len(Pxx) == 0:
            return round((freqs[min_freq_limit_index] - freqs[min_freq_limit_index] % 10)/1000.0, self.decimal_places)

        value = np.amax(Pxx) * np.power(10, self.threshold / 10.0)

        if self.total:
            min_freq_index = np.argwhere(Pxx >= value).min()

        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[peak_index:] = False
            min_freq_index = np.argwhere(below).max() + 1

        min_freq_index += min_freq_limit_index

        return round((freqs[min_freq_index] - freqs[min_freq_index] % 10)/1000.0, self.decimal_places)

    def get_visual_items(self):
        if isinstance(self.time_location, MeanMeasurementLocation):
            return [AverageFreqVisualItem(tooltip=self.tr(u"Max Freq") + u" at " + unicode(self.threshold) + u" dB->")]
        return []
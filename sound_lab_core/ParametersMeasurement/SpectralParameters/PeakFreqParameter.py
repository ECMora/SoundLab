# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import numpy as np
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import SpectralParameter


class PeakFreqParameter(SpectralParameter):
    """
    Class that measure the peak freq parameter on a segment
    """

    def __init__(self, decimal_places=2, time_measurement_location=None):
        SpectralParameter.__init__(self, decimal_places=decimal_places,
                                   time_measurement_location=time_measurement_location)
        self.name = "PeakFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        min_freq_index, max_freq_index = self.spectral_location.get_freq_limits(freqs)

        Pxx = Pxx[min_freq_index:max_freq_index]

        if len(Pxx) == 0:
            return round((freqs[min_freq_index] % 10) / 1000.0, self.decimal_places)

        index = np.argmax(Pxx)

        index += min_freq_index

        return round((freqs[index] - freqs[index] % 10) / 1000.0, self.decimal_places)

    def get_visual_items(self):
        if isinstance(self.time_location, MeanMeasurementLocation):
            return [AverageFreqVisualItem(QtGui.QColor(255, 50, 50, 255), tooltip=self.tr(u"Peak Freq"))]
        return []
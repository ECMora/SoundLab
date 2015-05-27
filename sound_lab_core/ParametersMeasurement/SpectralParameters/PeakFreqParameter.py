# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from numpy import argmax
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Locations.MeanMeasurementLocation import MeanFrequencyMeasurementLocation
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import SpectralParameter


class PeakFreqParameter(SpectralParameter):
    """
    Class that measure the peak freq parameter on a segment
    """

    def __init__(self, decimal_places=2, measurement_location=None):
        SpectralParameter.__init__(self, decimal_places=decimal_places, measurement_location=measurement_location)
        self.name = "PeakFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.location.get_segment_data(segment)
        index = argmax(Pxx)
        return round((freqs[index] - freqs[index] % 10) / 1000.0, self.decimal_places)

    def get_visual_items(self):
        if isinstance(self.location, MeanFrequencyMeasurementLocation):
            return [AverageFreqVisualItem(QtGui.QColor(255, 50, 50, 255), tooltip=self.tr(u"Peak Freq"))]
        return []
# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from FreqParameterAdapter import FreqParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.MaxFreqParameter import MaxFreqParameter


class MaxFreqParameterAdapter(FreqParameterAdapter):
    """
    Adapter class for the max freq parameter.
    """

    def __init__(self):
        FreqParameterAdapter.__init__(self)
        self.name = self.tr(u'MaxFreq')

    def get_instance(self):
        self.compute_settings()
        return MaxFreqParameter(threshold=self.threshold, total=self.total)

    def get_visual_items(self):
        return [AverageFreqVisualItem(tooltip=self.tr(u"Max Freq") + u" at " + unicode(self.threshold) + u" dB->")]



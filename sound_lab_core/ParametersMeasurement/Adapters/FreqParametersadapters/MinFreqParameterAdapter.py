# -*- coding: utf-8 -*-
from graphic_interface.segment_visualzation.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    FreqParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.MinFreqParameter import MinFreqParameter


class MinFreqParameterAdapter(FreqParameterAdapter):
    """
    Adapter class for the max freq parameter.
    """

    def __init__(self):
        FreqParameterAdapter.__init__(self)

    def get_instance(self):
        self.compute_settings()
        return MinFreqParameter(threshold=self.threshold,total=self.total)

    def get_visual_item(self):
        return AverageFreqVisualItem(tooltip=self.tr(u"Min Freq") + u" at " + unicode(self.threshold) + u"dB->")


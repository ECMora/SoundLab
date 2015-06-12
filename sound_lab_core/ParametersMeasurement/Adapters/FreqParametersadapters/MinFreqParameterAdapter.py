# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
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
        self.name = self.tr(u'MinFreq')

    def get_instance(self):
        self.compute_settings()

        visual_items = [AverageFreqVisualItem(color=self.visual_item_color,
                        tooltip=self.tr(u"Min Freq") + u" at " + unicode(self.threshold) + u"dB->")]

        return MinFreqParameter(threshold=self.threshold, total=self.total,
                                decimal_places=self.decimal_places, visual_items=visual_items)

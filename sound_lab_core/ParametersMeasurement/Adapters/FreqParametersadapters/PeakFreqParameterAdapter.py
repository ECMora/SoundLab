# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    SpectralParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeakFreqParameter import PeakFreqParameter


class PeakFreqParameterAdapter(SpectralParameterAdapter):
    """
    Adapter class for the peak freq parameter.
    """

    def __init__(self):
        SpectralParameterAdapter.__init__(self)
        self.name = self.tr(u'PeakFreq')

    def get_instance(self):
        self.compute_settings()
        visual_items = []

        if self.show_visual_items:
            visual_items = [AverageFreqVisualItem(color=self.visual_item_color, tooltip=self.tr(u"Peak Freq"),
                                                  connect_points=False, point_figure=self.items_figure,
                                                  points_size=self.items_pixel_size)]

        return PeakFreqParameter(decimal_places=self.decimal_places, visual_items=visual_items)
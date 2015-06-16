# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pyqtgraph.parametertree import Parameter
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
        visual_items = [] if not self.show_visual_items else [AverageFreqVisualItem(color=self.visual_item_color,
                                                                                    tooltip=self.tr(u"Peak Freq"))]

        return PeakFreqParameter(decimal_places=self.decimal_places, visual_items=visual_items)
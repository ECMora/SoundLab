# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.AverageFreqVisualItem import AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeakFreqParameter import PeakFreqParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class PeakFreqParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the peak freq parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)
        self.name = self.tr(u'PeakFreq')


    def get_instance(self):
        return PeakFreqParameter()

    def get_visual_items(self):
        return [AverageFreqVisualItem(QtGui.QColor(255, 50, 50, 255), tooltip=self.tr(u"Peak Freq"))]

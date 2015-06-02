# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.time_parameter_items.PeakToPeakVisualItem import PeakToPeakVisualItem
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.PeakToPeakParameter import PeakToPeakParameter


class PeakToPeakParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self.name = self.tr(u'PeakToPeak')

    def get_instance(self):
        return PeakToPeakParameter()

    def get_visual_items(self):
        return [PeakToPeakVisualItem()]

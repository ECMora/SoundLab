# -*- coding: utf-8 -*-
from graphic_interface.segment_visualization.parameter_items.time_parameter_items.PeakToPeakVisualItem import PeakToPeakVisualItem
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.PeakToPeakParameter import PeakToPeakParameter


class PeakToPeakParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'PeakToPeak')

    def get_instance(self):
        self.compute_settings()

        return PeakToPeakParameter(self.decimal_places)

    def get_visual_items(self):
        return [PeakToPeakVisualItem()]

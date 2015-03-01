# -*- coding: utf-8 -*-
from graphic_interface.segment_visualzation.parameter_items.time_parameter_items.PeakToPeakVisualItem import PeakToPeakVisualItem
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.PeakToPeakParameter import PeakToPeakParameter


class PeakToPeakParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_instance(self):
        return PeakToPeakParameter()

    def get_visual_item(self):
        return PeakToPeakVisualItem()

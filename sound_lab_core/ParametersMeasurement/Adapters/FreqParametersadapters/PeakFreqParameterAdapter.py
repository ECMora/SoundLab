# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeakFreqParameter import PeakFreqParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class PeakFreqParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the peak freq parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

    def get_instance(self):
        return PeakFreqParameter()

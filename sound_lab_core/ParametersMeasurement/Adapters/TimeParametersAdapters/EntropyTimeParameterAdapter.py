# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.EntropyTimeParameter import EntropyTimeParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class EntropyTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_instance(self):
        return EntropyTimeParameter()

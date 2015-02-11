# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.EndTimeParameter import EndTimeParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class EndTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        self.adapted_class = EndTimeParameter

    def get_settings(self):
        return []

    def apply_settings_change(self, transform, change):
        pass
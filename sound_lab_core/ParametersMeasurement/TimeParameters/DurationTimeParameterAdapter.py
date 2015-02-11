# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.DurationTimeParameter import DurationTimeParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class DurationTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        self.adapted_class = DurationTimeParameter

    def get_settings(self):
        return []

    def apply_settings_change(self, transform, change):
        pass
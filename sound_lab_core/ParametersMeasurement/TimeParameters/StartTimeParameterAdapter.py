# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.StartTimeParameter import StartTimeParameter


class StartTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        self.adapted_class = StartTimeParameter

    def get_settings(self):
        """
        :type parameter:
        """
        return []

    def apply_settings_change(self, transform, change):
        """

        :type transform:
        """
        pass
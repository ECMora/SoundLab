# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.EndTimeParameter import EndTimeParameter


class EndTimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        ParameterAdapter.__init__(self, parent)

        self.parameter_class = EndTimeParameter

    def get_settings(self, parameter):
        """
        :type parameter:
        """
        return []

    def apply_settings_change(self, transform, change):
        pass
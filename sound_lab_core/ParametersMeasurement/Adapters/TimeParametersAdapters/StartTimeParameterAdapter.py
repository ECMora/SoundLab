# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.StartTimeParameter import StartTimeParameter


class StartTimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)

    def get_instance(self):
        return StartTimeParameter()

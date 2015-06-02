# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.TimeParameterAdapter import \
    TimeParameterAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.EndTimeParameter import EndTimeParameter


class EndTimeParameterAdapter(TimeParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        TimeParameterAdapter.__init__(self)
        self.name = self.tr(u'End Time')


    def get_instance(self):
        self.compute_settings()

        return EndTimeParameter(self.decimal_places)


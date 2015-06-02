# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.RmsTimeParameter import RmsTimeParameter


class RmsTimeParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'RMS')

    def get_instance(self):
        self.compute_settings()

        return RmsTimeParameter(self.decimal_places)


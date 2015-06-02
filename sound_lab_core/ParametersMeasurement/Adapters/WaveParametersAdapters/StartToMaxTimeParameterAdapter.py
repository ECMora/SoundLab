# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.StartToMaxTimeParameter import StartToMaxTimeParameter


class StartToMaxTimeParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'StartToMax')

    def get_instance(self):
        self.compute_settings()

        return StartToMaxTimeParameter(self.decimal_places)

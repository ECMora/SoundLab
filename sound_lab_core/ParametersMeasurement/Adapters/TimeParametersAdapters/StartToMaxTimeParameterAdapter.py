# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.StartToMaxTimeParameter import StartToMaxTimeParameter


class StartToMaxTimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self.name = self.tr(u'StartToMax')

    def get_instance(self):
        return StartToMaxTimeParameter()

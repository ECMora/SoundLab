# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.EntropyTimeParameter import EntropyTimeParameter


class EntropyTimeParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'Entropy')

    def get_instance(self):
        self.compute_settings()

        return EntropyTimeParameter(self.decimal_places)

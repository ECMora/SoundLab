# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.ZeroCrossRateParameter import ZeroCrossRateParameter


class ZeroCrossRateParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the Zero cross rate time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'Zero Cross Rate')

    def get_instance(self):
        self.compute_settings()

        return ZeroCrossRateParameter(self.decimal_places)
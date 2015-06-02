# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.LocalMaxMeanParameter import LocalMaxMeanParameter


class LocalMaxMeanParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the local max mean time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = self.tr(u'Local Max Mean')

    def get_instance(self):
        self.compute_settings()

        return LocalMaxMeanParameter(self.decimal_places)





# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.FourierParametersAdapters.FourierParameterAdapter import \
    FourierParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.FourierParameters import SpectralRollOffParameter


class SpectralRollOffParameterAdapter(FourierParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        FourierParameterAdapter.__init__(self)
        self.name = self.tr(u"Spectral Roll-Off")

    def get_instance(self):
        self.compute_settings()
        return SpectralRollOffParameter(self.func, self.function_name)





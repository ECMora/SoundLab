# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.FourierParametersAdapters.FourierParameterAdapter import \
    FourierParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.FourierParameters import SpectrumSpreadParameter


class SpectrumSpreadParameterAdapter(FourierParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        FourierParameterAdapter.__init__(self)
        self.name = self.tr(u"Spectrum Spread")

    def get_instance(self):
        self.compute_settings()
        return SpectrumSpreadParameter(self.func, self.function_name, decimal_places=self.decimal_places)





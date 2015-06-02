# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.FourierParametersAdapters.FourierParameterAdapter import \
    FourierParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.FourierParameters import SpectralCentroidParameter


class SpectralCentroidParameterAdapter(FourierParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        FourierParameterAdapter.__init__(self)
        self.name = self.tr(u"Spectral Centroid")

    def get_instance(self):
        self.compute_settings()
        return SpectralCentroidParameter(self.func, self.function_name)





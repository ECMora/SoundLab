# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.FourierParameters.SpectralCentroidParameter import SpectralCentroidParameter


class SpectralCentroidParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, func, funcName):
        ParameterAdapter.__init__(self)
        self.func = func
        self.funcName = funcName

    def get_instance(self):
        return SpectralCentroidParameter(self.func, self.funcName)





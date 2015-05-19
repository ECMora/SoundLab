# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.ZeroCrossRateParameter import ZeroCrossRateParameter
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter


class ZeroCrossRateParameterAdapter(ParameterAdapter):
    """
    Adapter class for the Zero cross rate time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self.name = self.tr(u'Zero Cross Rate')


    def get_instance(self):
        return ZeroCrossRateParameter()





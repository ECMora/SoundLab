# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters import LocalMaxMeanParameter


class LocalMaxMeanParameterAdapter(ParameterAdapter):
    """
    Adapter class for the local max mean time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self.name = self.tr(u'Local Max Mean')

    def get_instance(self):
        return LocalMaxMeanParameter()





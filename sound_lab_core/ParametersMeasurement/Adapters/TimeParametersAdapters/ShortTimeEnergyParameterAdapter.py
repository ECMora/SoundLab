# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters import ShortTimeEnergyParameter


class ShortTimeEnergyParameterAdapter(ParameterAdapter):
    """
    Adapter class for the Zero cross rate time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)

    def get_instance(self):
        return ShortTimeEnergyParameter()





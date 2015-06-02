# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveParametersAdapters.WaveParameterAdapter import \
    WaveParameterAdapter
from sound_lab_core.ParametersMeasurement.WaveParameters.ShortTimeEnergyParameter import ShortTimeEnergyParameter


class ShortTimeEnergyParameterAdapter(WaveParameterAdapter):
    """
    Adapter class for the Zero cross rate time parameter.
    """

    def __init__(self):
        WaveParameterAdapter.__init__(self)
        self.name = u"ShortTimeEnergy"

    def get_instance(self):
        self.compute_settings()

        return ShortTimeEnergyParameter(self.decimal_places)





# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.SpectralParameters.BandWidthParameter import BandWidthParameter
from FreqParameterAdapter import FreqParameterAdapter


class BandWidthParameterAdapter(FreqParameterAdapter):
    """
    Adapter class for the band width parameter.
    """

    def __init__(self):
        FreqParameterAdapter.__init__(self)
        self.name = self.tr(u'BandWidth')

    def get_instance(self):
        self.compute_settings()
        return BandWidthParameter(threshold=self.threshold, total=self.total)
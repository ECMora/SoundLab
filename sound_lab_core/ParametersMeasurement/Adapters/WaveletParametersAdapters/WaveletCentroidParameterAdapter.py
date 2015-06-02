# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveletParametersAdapters.WaveletParameterAdapter import WaveletParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.WaveletParameters import WaveletCentroidParameter


class WaveletCentroidParameterAdapter(WaveletParameterAdapter):
    """
    Adapter class for the peaks above parameter.
    """

    def __init__(self):
        WaveletParameterAdapter.__init__(self)
        self.name = "WaveletCentroid"

    def get_instance(self):
        self.compute_settings()
        try:
            wavelet = self.settings.param(unicode(self.tr(u'Wavelet'))).value()

        except Exception as e:
            wavelet = self.wavelet

        self.wavelet = wavelet
        return WaveletCentroidParameter(level=self.level, wavelet=self.wavelet, decimal_places=self.decimal_places)

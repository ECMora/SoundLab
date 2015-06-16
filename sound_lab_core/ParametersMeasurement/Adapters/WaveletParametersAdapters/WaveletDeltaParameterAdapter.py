# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.WaveletParametersAdapters.WaveletParameterAdapter import WaveletParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.WaveletParameters import WaveletDeltaParameter


class WaveletDeltaParameterAdapter(WaveletParameterAdapter):
    """

    """

    def __init__(self):
        WaveletParameterAdapter.__init__(self)
        self.name = "WaveletDelta"

    def get_instance(self):
        self.compute_settings()
        try:
            wavelet = self.settings.param(unicode(self.tr(u'Wavelet'))).value()

        except Exception as e:
            wavelet = self.wavelet

        self.wavelet = wavelet
        return WaveletDeltaParameter(level=self.level, wavelet=self.wavelet, decimal_places=self.decimal_places)

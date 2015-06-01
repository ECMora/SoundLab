# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.WaveletParameters import WaveletVarParameter
from sound_lab_core.ParametersMeasurement.Adapters.WaveletParametersAdapters.WaveletParameterAdapter import WaveletParameterAdapter


class WaveletVarParameterAdapter(WaveletParameterAdapter):
    """
    Adapter class for the peaks above parameter.
    """

    def __init__(self):
        WaveletParameterAdapter.__init__(self)

    def __init__(self, level):
        WaveletParameterAdapter.__init__(self)
        self.level = level

    def get_instance(self):
        try:
            wavelet = self.settings.param(unicode(self.tr(u'Wavelet'))).value()

        except Exception as e:
            wavelet = self.wavelet

        self.wavelet = wavelet
        return WaveletVarParameter(level=self.level, wavelet=self.wavelet)

# -*- coding: utf-8 -*-
from duetto.dimensional_transformations.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
import matplotlib.mlab as mlab
import numpy as np

class InstantFrequencies(OneDimensionalTransform):
    """
    This is a class inherited from OneDimensionalTransform that specifies the
    maximo instant frequencies computation and properties
    """
    def __init__(self, signal=None, window=WindowFunction.Hamming, NFFT=512, overlap=0):
        OneDimensionalTransform.__init__(self, signal=None)

        self._window = window
        self._overlap = overlap
        self._NFFT = NFFT

    #region Properties NFFT , window, overlap

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def overlap(self):
        return self._overlap

    @overlap.setter
    def overlap(self, value):
        self._overlap = value

    @property
    def NFFT(self):
        return self._NFFT

    @NFFT.setter
    def NFFT(self, value):
        self._NFFT = value

    #endregion

    # def computeData(self, indexFrom, indexTo):
    #     data = self.signal.data[indexFrom:indexTo]
    #
    #     Pxx, freqs, bins = mlab.specgram(data, Fs=self.signal.samplingRate, window=self.window, NFFT=self.NFFT, noverlap=self.NFFT * self.overlap/100)
    #     dtemp =  freqs[np.argmax(Pxx[1:len(Pxx)], axis=0)]
    #
    #     self.data = (bins[dtemp>0],dtemp[dtemp>0]/1000)

    def getData(self, indexFrom, indexTo):

        minx = indexFrom
        maxx = max(indexTo, min(minx + self.NFFT, len(self.signal.data)))

        data = self.signal.data[indexFrom:indexTo]

        Pxx, freqs, bins = mlab.specgram(data, Fs=self.signal.samplingRate, window=self.window, NFFT=self.NFFT, noverlap=self.NFFT * self.overlap/100)
        dtemp =  freqs[np.argmax(Pxx[1:len(Pxx)], axis=0)]

        return (bins[dtemp>0],dtemp[dtemp>0]/1000)
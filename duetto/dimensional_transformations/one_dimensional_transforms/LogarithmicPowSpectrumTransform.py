# -*- coding: utf-8 -*-
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.dimensional_transformations.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np

class LogarithmicPowSpec(OneDimensionalTransform):
    """
    This is a class inherited from OneDimensionalTransform that specifies
    the logarithmic power spectrum computation and properties
    """
    def __init__(self, signal=None, window=WindowFunction.Hamming):
        OneDimensionalTransform.__init__(self, signal=signal)
        self._window = window

    #region Property window

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    #endregion

    def getData(self, indexFrom, indexTo):

        # minx = indexFrom
        # maxx = max(indexTo, min(minx + self.NFFT, len(self.signal.data)))
        data = self.signal.data[indexFrom:indexTo]

        windowVals = self.window(np.ones((len(data),), data.dtype))
        #apply the window function to the result
        dataWindowed = windowVals * data


        Px = abs(np.fft.fft(dataWindowed, 2**int(np.ceil(np.log2(len(data))))))[0:len(data)//2+1]
        freqs = float(self.signal.samplingRate) / len(data) * np.arange(len(data)//2+1)

        db = 10*np.log10(Px/np.amax(Px))

        return (freqs/1000, db)
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.dimensional_transformations.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np
import matplotlib.mlab as mlab

class AveragePowSpec(OneDimensionalTransform):
    """
    This is a class inherited from OneDimensionalTransform that specifies the
    average power spectrum computation and properties
    """
    def __init__(self, signal=None, window=WindowFunction.Hamming, NFFT=512, overlapRatio=0):
        OneDimensionalTransform.__init__(self, signal=signal)

        self._window = window
        self._NFFT = NFFT
        self._overlapRatio = overlapRatio

    #region Properties NFFT , window, overlap

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def overlapRatio(self):
        return self._overlapRatio

    @overlapRatio.setter
    def overlapRatio(self, value):
        self._overlapRatio = value

    @property
    def NFFT(self):
        return self._NFFT

    @NFFT.setter
    def NFFT(self, value):
        self._NFFT = value

    #endregion

    def __getOverlap(self, overlap_percent):
        """
        get the number of points of overlap from the percent value supplied.
        :param overlap_percent: the percent of overlap form the NFFT value.
        :return:
        """
        return self.NFFT * self.overlapRatio

    def getData(self, indexFrom, indexTo):

        data = self.signal.data[indexFrom:indexTo]
        overlap = self.NFFT * self.overlapRatio/100
        (Pxx, freqs) = mlab.psd(data,Fs=self.signal.samplingRate, NFFT=self.NFFT, window=self.window,
                                       noverlap=overlap, scale_by_freq=False)
        Pxx.shape = len(freqs)

        return (freqs/1000, 10*np.log10(Pxx/np.amax(Pxx)))
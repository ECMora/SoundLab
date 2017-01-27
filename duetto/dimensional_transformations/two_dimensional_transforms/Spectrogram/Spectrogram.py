# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from duetto.audio_signals import AudioSignal
import matplotlib.mlab as mlab
import numpy as np
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction


class Spectrogram(object):
    """
    Class that computes an spectrogram from an AudioSignal.
    """

    # region CONSTANTS
    # configuration variable for spectrogram creation could be "onesided" or "twosided"
    # onesided compute an spectrogram without complex side.
    SPECGRAM_COMPLEX_SIDE = "onesided"

    # Decimal places to round the time information
    # of an x-time position of the spectrogram
    TIME_DATA_DECIMAL_PLACES = 4

    # Decimal places to round the frequency information
    # of an y-time position of the spectrogram
    FREQ_DATA_DECIMAL_PLACES = 1

    # Decimal places to round the amplitude information
    # of an x,y (time, frequency) position of the spectrogram
    AMPLITUDE_DATA_DECIMAL_PLACES = 2

    # endregion

    def __init__(self, signal=None, NFFT=512, overlap=500, window=None, indexFrom=0, indexTo=-1):
        """
        Creates the object to compute spectrograms for signal AudioSignal
        :param NFFT: FFT number of points for spectral analysis.
        :param overlap: overlap points between two consecutives analysis intervals
        :param window: signal processing windows applied for each interval
        :param signal: Signal to process.
        :param indexFrom: beginning of the range to compute spectrogram
        :param indexTo: end of the range to compute spectrogram
        """
        if NFFT <= 0:
            raise Exception("NFFT must be positive.")
        if overlap < 0 or overlap >= NFFT:
            raise Exception("Overlap must be non negative and lower than NFFT.")

        if indexTo == -1:
            indexTo = 0 if signal is None else signal.length

        self._signal = signal
        self._NFFT = NFFT
        self.__overlap = overlap
        self.__visual_overlap = overlap
        self.__window = window if window is not None else WindowFunction.Hanning

        # internal data for spectrogram
        self.matriz = None #Pxx
        self.freqs = []
        self.bins = []

        # variables that store the last time interval of spectrogram computation
        self.lastInterval = (indexFrom, indexTo)
        self.lastMaxCol = None

        # variable for optimization on compute spectrogram
        self.changes = False

    # region Signal and data props
    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, newSignal):
        """
        The property to change the current signal.
        All internal variables are updated to deal with the new signal and to
        compute it's spectrogram.
        :param signal: the new Audio Signal.
        """
        if newSignal is None or not isinstance(newSignal,AudioSignal):
            raise Exception("Invalid assignation. Must be of type AudioSignal")

        self._signal = newSignal

        # update values for other processing or visualizing options
        self.changes = True
        # update the matrix, bins  and freqs for the new signal
        # self.recomputeSpectrogram()


    @property
    def NFFT(self):
        """
        Gets the FFT size
        :return: an integer, the amount of points used to calculate the FFTs for the spectrogram
        """
        return self._NFFT

    @NFFT.setter
    def NFFT(self, NFFT):
        """
        Sets the size of the FFT to NFFT points and recomputes the spectrogram
        :param NFFT: an integer, the amount of points to use to calculate the spectrogram
        """
        if NFFT == self._NFFT:
            return
        self._NFFT = NFFT

        self.changes = True

    @property
    def overlap(self):
        """
        Gets the number of points of overlap.
        :return: an integer, the number of points of overlap between two consecutive FFTs
        """
        return self.__overlap

    @overlap.setter
    def overlap(self, overlap):
        """
        Sets the number of points of overlap between two FFTs.
        :param overlap: an integer, the number of points to use as overlap between two consecutive FFTs
        """
        overlap = int(overlap)
        if overlap == self.__overlap:
            return
        self.__overlap = overlap
        self.changes = True

    def get_overlap_ratio(self):
        """
        Gets the overlap as a fraction of the FFT size.
        :return: a float between 0 and 1, the overlap as a fraction of the FFT size
        """
        return 1.0 * self.overlap / self.NFFT

    def set_overlap_ratio(self, ratio):
        """
        Sets the overlap to be a given fraction of the FFT size.
        :param ratio: a float between 0 and 1 indicating the fraction of the FFT size to which the overlap must be set
        """
        self.overlap = 1.0 * self.NFFT * ratio

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        if window == self.__window:
            return
        self.__window = window
        self.changes = True

    # endregion

    def recomputeSpectrogram(self, indexFrom=None, indexTo=None, maxCol=None):
        """
        Method that computes the spectrogram of the signal in the supplied interval
        :param indexFrom: Start index in signal data array coordinates
        :param indexTo: End index in signal data array coordinates
        """

        # do not work fine if the signal data changes
        # if not self.changes and self.lastInterval == (indexFrom, indexTo):
        # return

        indexFrom = indexFrom if indexFrom is not None else self.lastInterval[0]

        indexTo = indexTo if indexTo is not None else self.lastInterval[1]

        indexTo = indexTo if indexTo != -1 else self.signal.length

        maxCol = maxCol if maxCol != 0 else self.signal.length/self.NFFT

        if self.signal is None:
            raise Exception("No signal to compute spectrogram")

        # computing overlap so the number of columns is less or equal than maxCol
        smin = indexFrom - self.NFFT
        smax = indexTo + self.NFFT
        pre, post = np.zeros(max(-smin, 0)), np.zeros(max(smax - self.signal.length, 0))
        data = np.concatenate((pre, self.signal.data[max(smin, 0): min(smax, self.signal.length)], post))

        self.__visual_overlap = self.overlap
        if maxCol is not None:
            cs = self.NFFT - self.overlap
            cols = (smax - smin - self.overlap) / cs
            if cols > maxCol:
                self.__visual_overlap = int(self.NFFT - (smax - smin) / maxCol)

        if False and indexFrom == self.lastInterval[0] and indexTo == self.lastInterval[1]:
            return

        # delegate in matplotlib specgram function the process of compute the spectrogram
        self.matriz, self.freqs, self.bins = mlab.specgram(
            data, NFFT=self.NFFT,
            Fs=self.signal.samplingRate, detrend=mlab.detrend_none,
            window=self.window, noverlap=self.__visual_overlap,
            sides=self.SPECGRAM_COMPLEX_SIDE)

        # changes to dB for bio acoustic processing
        temp = np.amax(self.matriz)
        if temp == 0:
            temp = 1.0
        self.matriz = 10. * np.log10(self.matriz / temp)
        Zfin = np.isfinite(self.matriz)
        if np.any(Zfin):
            m = self.matriz[Zfin].min()
            self.matriz[np.isneginf(self.matriz)] = m
        else:
            self.matriz[self.matriz < -100] = -100 # verificar estos valores constantes
        self.matriz = np.transpose(self.matriz)
        self.lastInterval = (indexFrom, indexTo)
        self.lastMaxCol = maxCol
        self.changes = False

    def from_spec_to_osc(self, coord):
        """
        This function converts an spectrogram sample to the corresponding oscillogram sample
        :param coord: spectrogram sample number
        :return: oscillogram sample number
        """

        cs = self.NFFT - self.__visual_overlap
        return self.lastInterval[0] + (1.0 * coord * cs - self.NFFT / 2.0)

    def from_osc_to_spec(self, coord):
        """
        This function converts an oscillogram sample to the corresponding spectrogram sample
        :param coord: oscillogram sample number
        :return: spectrogram sample number
        """
        cs = self.NFFT - self.__visual_overlap

        if self.lastInterval[0] > coord:
            return 0

        elif self.lastInterval[1] < coord:
            return len(self.bins)

        return 1.0 * (coord - self.lastInterval[0] + self.NFFT/2) / cs

    def get_freq_index(self, freq):
        """
        Gets the index (or indices) in the spectrogram matrix of the corresponding frequency (or frequencies)
        :param freq: number or array_like, the frequency value(s) whose index is to be known
        :return: int or array_like of ints, the wanted index (or indices)
        """
        return -1 if len(self.freqs) == 0 else np.searchsorted(self.freqs, freq)

    def getInfo(self, x, y):
        """
        This function returns the time, frequency and amplitude values of an spectrogram point.
        :param x: spectrogram sample number
        :param y: frequency index
        :return:
        """
        if len(self.freqs) == 0:
            # or must raise exception ?
            return [0, 0, 0]

        if y < 0:
            y = 0
        if y >= len(self.freqs):
            y = len(self.freqs) - 1

        time = np.round(self.from_spec_to_osc(x) * 1.0 / self.signal.samplingRate, self.TIME_DATA_DECIMAL_PLACES)
        freq = np.round(self.freqs[y] * 1.0 / 1000, self.FREQ_DATA_DECIMAL_PLACES)
        intensity = np.round(self.matriz[x][y], self.AMPLITUDE_DATA_DECIMAL_PLACES)
        return [time, freq, intensity]

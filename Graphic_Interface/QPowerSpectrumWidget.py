from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy
from matplotlib import mlab


class QPowerSpectrumWidget(FigureCanvas):
    def __init__(self, parent=None):

        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.set_facecolor('w')

    def get_highest_freq(self):
        index = []
        maxdb = self.Pxx[1]
        for i in range(2,len(self.Pxx)):
            if maxdb < self.Pxx[i]:
                maxdb = self.Pxx[i]
                index = []
            if maxdb ==self.Pxx[i]:
                index.append(self.freqs[i])
        return index , maxdb

    def Plot_Power_Spectrum(self, data, Fs, NFFT, window):
        self.pow_spectrum = self.fig.add_subplot(111)
        if window == "Hanning":
            window = mlab.window_hanning
        else:
            window= mlab.window_none
        (self.Pxx , self.freqs) = self.pow_spectrum.psd(data,Fs= Fs,NFFT=NFFT, window=window)
        self.pow_spectrum.set_xlim(0,Fs/2)
        (max_freq, maxdb) = self.get_highest_freq()
        x = [max_freq, max_freq]
        y = [10 * numpy.log10(min(self.Pxx)), 10 * numpy.log10(maxdb)]
        self.pow_spectrum.hold(True)
        self.pow_spectrum.plot(x,y)
        self.pow_spectrum.set_xlabel("Frequency(Hz)")
        self.pow_spectrum.set_ylabel("Intensity(dB/Hz)")

        self.draw()
        return self.Pxx, self.freqs

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy
import pyqtgraph as pg
from matplotlib import mlab


class QPowerSpectrumWidget(QtGui.QWidget):
    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setParent(parent)

    def get_highest_freq(self):
        return  self.freqs[numpy.argmax(self.Pxx[1:len(self.Pxx)], axis=0)]

    def Plot_Power_Spectrum(self, data, Fs, NFFT, window):

        self.pow_spectrum = pg.PlotWidget(parent=self)
        (self.Pxx , self.freqs) = mlab.psd(data,Fs= Fs,NFFT=NFFT, window=window)
        self.Pxx.shape = len(self.freqs)
        self.pow_spectrum.plot(self.freqs,10*numpy.log10(self.Pxx))

        return self.Pxx, self.freqs
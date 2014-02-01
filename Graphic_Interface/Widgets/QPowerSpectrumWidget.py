#from PyQt4 import QtGui
#from matplotlib.backends.backend_qt4agg \
#    import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import numpy
#import pyqtgraph as pg
#from matplotlib import mlab
#
#
#class QPowerSpectrumWidget(FigureCanvas):
#    def __init__(self, parent=None):
#
#        self.fig = Figure()
#        FigureCanvas.__init__(self, self.fig)
#        self.setParent(parent)
#        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#        self.fig.set_facecolor('w')
#
#    def get_highest_freq(self):
#        return  self.freqs[numpy.argmax(self.Pxx[1:len(self.Pxx)], axis=0)]
#
#    def Plot_Power_Spectrum(self, data, Fs, NFFT, window):
#        self.fig.clear()
#        self.pow_spectrum = self.fig.add_subplot(111)
#        (self.Pxx , self.freqs) = self.pow_spectrum.psd(data,Fs= Fs,NFFT=NFFT, window=window)
#        self.pow_spectrum.set_xlim(0,Fs/2)
#        max_freq = self.get_highest_freq()
#        x = [max_freq, max_freq]
#        y = [10 * numpy.log10(min(self.Pxx)), 10 * numpy.log10(max(self.Pxx[1:len(self.Pxx)]))]
#        self.pow_spectrum.hold(True)
#        self.pow_spectrum.plot(x,y)
#        self.pow_spectrum.set_xlabel("Frequency(Hz)")
#        self.pow_spectrum.set_ylabel("Intensity(dB/Hz)")
#
#        self.draw()
#        return self.Pxx, self.freqs


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
        layout = QtGui.QVBoxLayout()

        self.setLayout(layout)
        self.setParent(parent)

    def get_highest_freq(self):
        return  self.freqs[numpy.argmax(self.Pxx[1:len(self.Pxx)], axis=0)]

    def Plot_Power_Spectrum(self, data, Fs, NFFT, window):

        self.pow_spectrum = pg.PlotWidget(parent=self)
        self.pow_spectrum.setFixedWidth(300)
        self.pow_spectrum.setFixedHeight(300)
        self.pow_spectrum.getPlotItem().enableAutoRange()
        (self.Pxx , self.freqs) = mlab.psd(data,Fs= Fs,NFFT=NFFT, window=window)
        self.Pxx.shape = len(self.freqs)
        self.pow_spectrum.plot(self.freqs,10*numpy.log10(self.Pxx))
        self.pow_spectrum.show()
        return self.Pxx, self.freqs
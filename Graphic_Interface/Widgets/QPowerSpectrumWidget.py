
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
        self.pow_spectrum = pg.PlotWidget(parent=self)
        self.pow_spectrum.getPlotItem().setMouseEnabled(False,False)
        self.pow_spectrum.getPlotItem().setLabel(axis='bottom',text='Frequency',units='Hz')
        self.pow_spectrum.getPlotItem().setLabel(axis='left', text='Intensity', units='db')
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.pow_spectrum)
        layout.setStretch(1,1)
        self.setLayout(layout)

    def get_highest_freq(self):
        return  self.freqs[numpy.argmax(self.Pxx[1:len(self.Pxx)], axis=0)]

    def Plot_Power_Spectrum(self, data, Fs, NFFT, window, plotColor, BackColor, gridX, gridY):

        self.pow_spectrum.getPlotItem().setTitle(title='NFFT '+str(NFFT) + ' ' + window.__name__)
        self.pow_spectrum.getPlotItem().hideButtons()
        (self.Pxx , self.freqs) = mlab.psd(data,Fs= Fs,NFFT=NFFT, window=window,scale_by_freq=False)
        self.Pxx.shape = len(self.freqs)
        self.pow_spectrum.setBackground(BackColor)
        self.pow_spectrum.getPlotItem().showGrid(x=gridX, y=gridY)
        self.pow_spectrum.plot(self.freqs,10*numpy.log10(self.Pxx/numpy.amax(self.Pxx)),clear=True, pen=plotColor)
        self.pow_spectrum.show()
        return self.Pxx, self.freqs
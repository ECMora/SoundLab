from matplotlib import mlab
import numpy
from Power_Spectrum import Ui_PowSpecWindow
from PyQt4 import QtGui,QtCore



class PowerSpectrumWindow(QtGui.QMainWindow):
    def __init__(self,parent=None,plotColor="FFF",backColor="FFF",gridx=True,gridy=True,minY=-50,maxY=5,lines=True):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.show()
        self.plotColor = plotColor
        self.backColor = backColor
        self.gridx = gridx
        self.gridy = gridy
        self.maxY = maxY
        self.minY = minY
	self.lines =lines

        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.Pxx = None
        self.freqs = None

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def plot(self, data, rate, NFFT, window,overlap):

        self.NFFT = NFFT
        self.window = window
        self.rate = rate
        self.overlap = overlap
        self.ui.widget.getPlotItem().setTitle(title='NFFT '+str(NFFT) + ' ' + window.__name__)
        self.ui.widget.getPlotItem().hideButtons()
        (self.Pxx , self.freqs) = mlab.psd(data,Fs= self.rate,NFFT=NFFT, window=window,noverlap=overlap,scale_by_freq=False)
        self.Pxx.shape = len(self.freqs)
        self.ui.widget.setInfo(self.Pxx,self.freqs)
        self.ui.widget.setBackground(self.backColor)
        self.ui.widget.getPlotItem().showGrid(x=self.gridx, y=self.gridy)
        self.ui.widget.plot(self.freqs,10*numpy.log10(self.Pxx/numpy.amax(self.Pxx)),clear=True, pen = self.plotColor if self.lines else None, symbol = 's', symbolSize = 1,symbolPen = self.plotColor)
        self.ui.widget.setRange(xRange = (0,self.freqs[len(self.freqs) - 1]),yRange=(self.maxY,self.minY),padding=0,update=True)
        self.ui.widget.show()

    def updatePowSpectrumInterval(self,data):
        self.plot(data,self.rate,self.NFFT,self.window,self.overlap)

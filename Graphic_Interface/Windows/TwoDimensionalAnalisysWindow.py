# -*- coding: utf-8 -*-
from PyQt4.QtGui import QFileDialog
from matplotlib import mlab
import numpy
from Graphic_Interface.Widgets.Power_Spectrum  import Ui_PowSpecWindow
from PyQt4 import QtGui,QtCore

class TwoDimensionalAnalisysWindow(QtGui.QMainWindow,Ui_PowSpecWindow):
    def __init__(self,parent=None,minY=-50,maxY=5,lines=True):
        super(TwoDimensionalAnalisysWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.plotColor = "FFF"
        self.maxY = maxY
        self.minY = minY
        self.lines =lines
        self.widget.getPlotItem().showGrid(x=True, y=True)

        self.widget.getPlotItem().hideButtons()
        self.Pxx = None
        self.freqs = None

    def load_Theme(self, theme):
        update_graph =False
        self.widget.setBackground(theme.pow_Back)

        if self.plotColor != theme.pow_Plot:
            self.plotColor = theme.pow_Plot
            update_graph =True

        self.widget.getPlotItem().showGrid(x=theme.pow_GridX, y=theme.pow_GridY)

        if update_graph:
            self.widget.update()

    def on_actionSave_Image_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save two dimensional graphics as an Image ","-Duetto-Image","*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(self.widget.winId())
            image.save(fname, 'jpg')


    def plot(self, data, rate, NFFT, window,overlap):
        self.NFFT = NFFT
        self.window = window
        self.rate = rate
        self.overlap = overlap
        #self.widget.getPlotItem().setTitle(title='NFFT '+str(NFFT) + ' ' + window.__name__)
        (self.Pxx , self.freqs) = mlab.psd(data,Fs= self.rate,NFFT=NFFT, window=window,noverlap=overlap,scale_by_freq=False)
        self.Pxx.shape = len(self.freqs)
        self.widget.setInfo(self.Pxx,self.freqs)
        self.widget.plot(self.freqs,10*numpy.log10(self.Pxx/numpy.amax(self.Pxx)),clear=True, pen = self.plotColor if self.lines else None, symbol = 's', symbolSize = 1,symbolPen = self.plotColor)
        self.widget.setRange(xRange = (0,self.freqs[len(self.freqs) - 1]),yRange=(self.maxY,self.minY),padding=0,update=True)
        #self.widget.show()


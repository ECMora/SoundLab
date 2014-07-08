# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy
from Graphic_Interface.Widgets.Power_Spectrum  import Ui_PowSpecWindow
from PyQt4 import QtGui,QtCore

class PowerSpectrumWindow(QtGui.QMainWindow,Ui_PowSpecWindow):
    def __init__(self,parent=None,minY=-50,maxY=5,lines=True):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.show()
        self.plotColor = "FFF"
        self.backColor = "000"
        self.gridx = True
        self.gridy = True
        self.maxY = maxY
        self.minY = minY
        self.lines =lines
        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.ui.widget.getPlotItem().showGrid(x=self.gridx, y=self.gridy)

        self.ui.widget.getPlotItem().hideButtons()
        self.Pxx = None
        self.freqs = None

    def load_Theme(self, theme):
        update_graph =False
        if self.backColor != theme.pow_Back:
            self.backColor = theme.pow_Back
            self.ui.widget.setBackground(self.backColor)

        if self.plotColor != theme.pow_Plot:
            self.plotColor = theme.pow_Plot
            update_graph =True

        if self.gridx != theme.pow_GridX or self.gridy != theme.pow_GridY:
            self.gridx = theme.pow_GridX
            self.gridy = theme.pow_GridY
            self.ui.widget.getPlotItem().showGrid(x=self.gridx, y=self.gridy)

        if update_graph:
            self.ui.widget.update()

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def plot(self, data, rate, NFFT, window,overlap):

        self.NFFT = NFFT
        self.window = window
        self.rate = rate
        self.overlap = overlap

        #self.Pxx , self.freqs = self.ui.widget.logarithmicProcessing(data, rate, window, self.plotColor, self.lines, self.maxY, self.minY)#rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)
        self.ui.widget.cepstrumProcessing(data, rate, window, self.plotColor, self.lines, self.maxY, self.minY)#rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)
        #self.Pxx , self.freqs = self.ui.widget.averageProcessing(data, rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)

    def updatePowSpectrumInterval(self,data):
        self.plot(data,self.rate,self.NFFT,self.window,self.overlap)

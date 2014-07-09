# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor,QColor
from matplotlib import mlab
import pyqtgraph as pg
import numpy
from Graphic_Interface.Widgets.Tools import Tools
from Axis import *
from Duetto_Core.SpecgramSettings import FFTWindows
import numpy as np
from Graphic_Interface.Widgets.Tools import RectROI

class OneDimensionalFunction:
    def __init__(self,widget):
        self.windows = FFTWindows()
        self.myOptions = {}
        self.widget = widget

    def connectMySignal(self,pTree):
        pass

    def processing(self):
        self.widget.lastProc = self.processing

class LogarithmicPowSpec(OneDimensionalFunction):
    def __init__(self,widget):
        OneDimensionalFunction.__init__(self,widget)
        self.myOptions = {u'name': u'Power spectrum(Logarithmic)', u'type': u'group', u'children': [
            {u'name': u'FFT window', u'type': u'list', u'value':self.windows.Hanning,u'default':self.windows.Hanning,
             u'values': [(u'Bartlett',self.windows.Bartlett),(u"Blackman", self.windows.Blackman),(u"Hamming", self.windows.Hamming), (u"Hanning", self.windows.Hanning),(u'Kaiser',self.windows.Kaiser),(u'None',self.windows.WindowNone),(u"Rectangular", self.windows.Rectangular)]},
            {u'name': u'Apply Function', u'type': u'action'},
        ]}

    def connectMySignal(self,pTree):
        self.pTree = pTree
        self.pTree.param('Power spectrum(Logarithmic)', 'Apply Function').sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalFunction.processing(self)
        window = self.pTree.param('Power spectrum(Logarithmic)', 'FFT window').value()
        #apply the window function to the result

        Px = abs(np.fft.fft(self.widget.data))[0:len(self.widget.data)//2+1]
        freqs = float(self.widget.Fs) / len(self.widget.data) * np.arange(len(self.widget.data)//2+1)
        self.Pxx = Px
        self.freqs = freqs
        self.widget.refresh(freqs, 10*numpy.log10(Px/numpy.amax(Px)))
        
class AveragePowSpec(OneDimensionalFunction):
        def __init__(self,widget):
            OneDimensionalFunction.__init__(self,widget)
            self.myOptions = {u'name': u'Power spectrum(Average)', u'type': u'group', u'children': [
            {u'name':u'FFT size', u'type': u'list', u'default':512, u'values': [(u'Automatic', 512),(u"128", 128), (u"256", 256),(u"512", 512), (u"1024", 1024)], u'value': u'512'},
            {u'name': u'FFT window', u'type': u'list', u'value':self.windows.Hanning,u'default':self.windows.Hanning,
             u'values': [(u'Bartlett',self.windows.Bartlett),(u"Blackman", self.windows.Blackman),(u"Hamming", self.windows.Hamming), (u"Hanning", self.windows.Hanning),(u'Kaiser',self.windows.Kaiser),(u'None',self.windows.WindowNone),(u"Rectangular", self.windows.Rectangular)]},
            {u'name': u'FFT overlap', u'type': u'int', u'value':90, u'limits': (-1, 99)},
            {u'name': u'Apply Function', u'type': u'action'},
        ]}

        def connectMySignal(self,pTree):
            self.pTree = pTree
            self.pTree.param('Power spectrum(Average)', 'Apply Function').sigActivated.connect(self.processing)

        def processing(self):
            OneDimensionalFunction.processing(self)
            window = self.pTree.param('Power spectrum(Average)', 'FFT window').value()
            NFFT = self.pTree.param('Power spectrum(Average)', 'FFT size').value()
            overlap = self.pTree.param('Power spectrum(Average)', 'FFT overlap').value()
            #apply the window function to the result

            (Pxx , freqs) = mlab.psd(self.widget.data, Fs= self.widget.Fs, NFFT=NFFT, window=window, noverlap=overlap, scale_by_freq=False)
            Pxx.shape = len(freqs)
            self.widget.Pxx = Pxx
            self.widget.freqs = freqs
            self.widget.refresh(freqs,10*numpy.log10(Pxx/numpy.amax(Pxx)))

class PowSpecPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None,**kargs):
        self.proc = [LogarithmicPowSpec(self),AveragePowSpec(self)]
        self.lastProc = None
        #self.axisXOsc = OscXAxis(self, orientation='bottom')
        #self.axisYOsc = OscYAxis(self, orientation='left')
        #kargs["axisItems"]={'bottom': self.axisXOsc, 'left': self.axisYOsc}
        pg.PlotWidget.__init__(self, **kargs)
        self.mousePressed = False
        pg.LegendItem()
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        #self.xLine = pg.InfiniteLine(angle = 90,pen=(0,9))
        #self.yLine = pg.InfiniteLine(angle = 0,pen=(0,9))
        #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.selectedTool = None

        self.getPlotItem().getViewBox().addItem(self.pointerCursor)
        #self.getPlotItem().getViewBox().addItem(self.xLine)
        #self.getPlotItem().getViewBox().addItem(self.yLine)
        self.getPlotItem().setMouseEnabled(False,False)
        self.getPlotItem().setLabel(axis='bottom',text='<font size=6>Frequency<\\font>',units='<font size=6>Hz<\\font>')
        self.getPlotItem().setLabel(axis='left', text='<font size=6>Intensity<\\font>', units='<font size=6>dB<\\font>')
        self.mouseReleased = False
        self.last = {}
        self.freqs =[]
        self.Pxx =[]

    PointerChanged = pyqtSignal(str)
    PointerCursorPressed = pyqtSignal()
    PIXELS_OF_CURSORS_CHANGES = 5

    def refresh(self,x,y):
        self.plot(x,y,clear=True, pen = self.plotColor if self.lines else None, symbol = 's', symbolSize = 1,symbolPen = self.plotColor)
        self.setRange(xRange = (0,x[len(x) - 1]),yRange=(self.maxY, self.minY),padding=0,update=True)
        self.setBackground(self.backColor)
        self.getPlotItem().showGrid(x=self.gridX, y=self.gridY)
        self.show()


    def updateLast(self,data):
        self.setData(data)
        self.lastProc()

    def setData(self,data):
        self.data = data

    def connectSignals(self,pTree):
        for proc in self.proc: proc.connectMySignal(pTree)

    def getParamsList(self):
        params = []
        for proc in self.proc: params.append(proc.myOptions)
        return params

    def clearPointerCursor(self):
        self.pointerCursor.clear()
        self.mouseReleased = False

    def mouseMoveEvent(self, event):

        if self.selectedTool == Tools.PointerCursor:
            if self.mousePressed:return

            (x,insidex) = self.fromCanvasToClient(event.x())
            (y,insidey) = self.fromCanvasToClientY(event.y())
            info = self.getFrequencyAmplitudeInfo(x)

            #self.xLine.setValue(info[0])
            #self.yLine.setValue(info[1])

            if self.mouseReleased:
                 info0 = self.getFrequencyAmplitudeInfo(self.last['pos'][0])
                 f0 = numpy.round(info0[0]/1000,1)
                 a0 = numpy.round(info0[1],1)
                 f1 = numpy.round(info[0]/1000,1)
                 a1 = numpy.round(info[1],1)
                 self.PointerChanged.emit(str.format('f0: {0}kHz  Amplitude0: {1}dB f1: {2}kHz Amplitude1: {3}dB df: {4}kHz dAmplitude: {5}dB',f0,a0 ,f1, a1,numpy.abs(f1-f0),numpy.abs(a1-a0)))
            else:
                self.PointerChanged.emit(str.format('Frecuencia: {0}kHz  Amplitud: {1}dB',numpy.round(info[0]/1000,1),numpy.round(info[1],1)))
            if not insidex or not insidey:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            else:
                self.setCursor(QCursor(QtCore.Qt.CrossCursor))
            self.update()

    def mousePressEvent(self, event):
        self.mousePressed = True
        if self.selectedTool == Tools.PointerCursor:
            self.pointerCursor.clear()
            (x,insidex) = self.fromCanvasToClient(event.x())
            info = self.getFrequencyAmplitudeInfo(x)
            if not insidex:
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))
                return
            self.last = {'pos':[info[0],info[1]], 'pen': {'color': 'w', 'width': 2},'brush':pg.intColor(255, 255), 'symbol':'+', 'size':20}
            self.pointerCursor.addPoints([self.last])
            self.mouseReleased = False
            self.PointerCursorPressed.emit()

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        if self.selectedTool == Tools.PointerCursor:
            self.mouseReleased = True

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        """
        vb = self.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    #PIXELS_BETWEEN_AXES_AND_DATA = 10 #the pixels for the numbers in the left side

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        inside = True
        vb = self.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a , b = self.viewRange()[0]
        if xPixel < minx:
            xPixel = minx
            inside = False
        if xPixel > maxx:
            xPixel = maxx
            inside = False
        return (a + int(round((xPixel - minx) * ( b - a ) * 1. / (maxx - minx), 0)) - 1,inside)

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        inside = True
        vb = self.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.getPlotItem().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            inside = False
            yPixel = miny
        if yPixel > maxy:
            inside = False
            yPixel = maxy
        return (a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0)), inside)

    def getFrequencyAmplitudeInfo(self,x):
        index = numpy.searchsorted(self.freqs,x)
        freq = self.freqs[index]
        amplt = 10*numpy.log10(self.Pxx[index]/numpy.amax(self.Pxx))
        return [freq, amplt]

    def loadTheme(self,Fs, window, plotColor,backColor, lines, maxY, minY, gridX, gridY):
        self.Fs = Fs
        self.window = window
        self.plotColor = plotColor
        self.lines = lines
        self.maxY = maxY
        self.minY = minY
        self.backColor = backColor
        self.gridX = gridX
        self.gridY = gridY

    #def averageProcessing(self, data, Fs, NFFT, window, noverlap, maxY, minY, plotColor, lines):
    #    (Pxx , freqs) = mlab.psd(data, Fs= Fs, NFFT=NFFT, window=window, noverlap=noverlap, scale_by_freq=False)
    #    Pxx.shape = len(freqs)
    #    self.Pxx = Pxx
    #    self.freqs = freqs
    #    self.plot(freqs,10*numpy.log10(Pxx/numpy.amax(Pxx)),clear=True, pen = plotColor if lines else None, symbol = 's', symbolSize = 1,symbolPen = plotColor)
    #    self.setRange(xRange = (0,freqs[len(freqs) - 1]),yRange=(maxY, minY),padding=0,update=True)
    #    self.show()
    #
    #def logarithmicProcessing(self, x, Fs, window, plotColor, lines, maxY, minY):
    #
    #    Px = abs(np.fft.fft(x))[0:len(x)//2+1]
    #    freqs = float(Fs) / len(x) * np.arange(len(x)//2+1)
    #    self.Pxx = Px
    #    self.freqs = freqs
    #    self.plot(freqs, 10*numpy.log10(Px/numpy.amax(Px)), clear=True, pen = plotColor if lines else None, symbol = 's', symbolSize = 1,symbolPen = plotColor)
    #    self.setRange(xRange = (0,freqs[len(freqs) - 1]),yRange=(maxY, minY),padding=0,update=True)
    #    self.show()
    #
    ##def cepstrumProcessing(self, x, Fs, window, plotColor, lines, maxY, minY):
    ##
    ##    Px = np.fft.fft(x)
    ##
    ##    out  = np.fft.ifft(10*numpy.log10(Px/numpy.amax(Px)),n=None, axis=-1)
    ##    time = []
    ##    for t in np.arange(0,len(out)):
    ##        time.append(t * 1.0 / Fs)
    ##
    ##    self.plot(time, out.real, clear=True, pen = plotColor if lines else None, symbol = 's', symbolSize = 1,symbolPen = plotColor)
    ##    self.show()
    ##    return out, time

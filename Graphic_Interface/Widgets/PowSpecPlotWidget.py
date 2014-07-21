# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor,QColor
from matplotlib import mlab
from PyQt4 import QtGui
import pyqtgraph as pg
from Graphic_Interface.Widgets.Tools import Tools
from Axis import *
from Duetto_Core.SpecgramSettings import FFTWindows
import numpy as np
from Graphic_Interface.Widgets.Tools import RectROI

class OneDimensionalFunction:
    def __init__(self,widget):
        self.myOptions = {}
        self.widget = widget
        self.windows = FFTWindows()

    def connectMySignal(self,pTree):
        self.pTree = pTree

    def processing(self):
        self.widget.mouseReleased = False
        self.widget.lastProc = self.processing
        self.widget.getInfo = self.getInfo
        self.widget.getStr = self.getStr
        self.widget.getStrPoint = self.getStrPoint
        self.widget.pointerCursor.clear()

    def getInfo(self,x):
        pass

    def getStr(self,info0, info1):
        pass

    def getStrPoint(self, info):
        pass

class LogarithmicPowSpec(OneDimensionalFunction):
    def __init__(self,widget):
        OneDimensionalFunction.__init__(self,widget)
        self.myOptions = {u'name': u'Power spectrum(Logarithmic)', u'type': u'group', u'children': [
            {u'name': u'FFT window', u'type': u'list', u'value':self.windows.Hamming, u'default':self.windows.Hamming,
             u'values': [(u'Hamming', self.windows.Hamming), (u'Bartlett',self.windows.Bartlett),(u'Blackman', self.windows.Blackman),(u'Hanning', self.windows.Hanning),(u'Kaiser',self.windows.Kaiser),(u'None',self.windows.WindowNone),(u"Rectangular", self.windows.Rectangular)]},
            {u'name': u'Apply Function', u'type': u'action'},
        ]}

    def connectMySignal(self,pTree):
        OneDimensionalFunction.connectMySignal(self,pTree)
        self.pTree.param('Power spectrum(Logarithmic)', 'Apply Function').sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalFunction.processing(self)

        minx = self.widget.rangeX[0]
        maxx = max(self.widget.rangeX[1], min(minx + self.widget.NFFTSpec, len(self.widget.data)))
        data = self.widget.data[minx:maxx]

        window = self.pTree.param('Power spectrum(Logarithmic)', 'FFT window').value()
        windowVals = window(np.ones((len(data),), data.dtype))
        dataWindowed = windowVals * data
        #apply the window function to the result

        Px = abs(np.fft.fft(dataWindowed, 2**int(np.ceil(np.log2(len(data))))))[0:len(data)//2+1]
        freqs = float(self.widget.Fs) / len(data) * np.arange(len(data)//2+1)

        self.widget.updateInterval(minx,maxx)
        self.widget.Pxx = Px
        self.widget.freqs = freqs
        db = 10*np.log10(Px/np.amax(Px))
        self.widget.plot(freqs/1000, db ,clear=True, pen = self.widget.plotColor, symbol = 's', symbolSize = 1,symbolPen = self.widget.plotColor)
        self.widget.setRange(xRange = (0,freqs[len(freqs) - 1]/1000),yRange = (np.amin(db),0), padding=0,update=True)
        self.widget.setBackground(self.widget.backColor)
        self.widget.getPlotItem().showGrid(x=self.widget.gridX, y=self.widget.gridY)
        self.widget.getPlotItem().setLabel(axis='bottom',text='<font size=6>Frequency<\\font>')
        self.widget.getPlotItem().setLabel(axis='left', text='<font size=6>Intensity<\\font>', units='<font size=6>dB<\\font>')
        self.widget.getPlotItem().setTitle(title='<font size=6>Power Spectrum (Logarithmic) <\\font>')
        self.widget.updateViewBox()
        self.widget.show()

    def getInfo(self,x):
        index = np.searchsorted(self.widget.freqs,x*1000)
        freq = self.widget.freqs[index]
        amplt = 10*np.log10(self.widget.Pxx[index]/np.amax(self.widget.Pxx))
        return [freq/1000, amplt]

    def getStr(self, info0, info1):
        f0 = np.round(info0[0],1)
        a0 = np.round(info0[1],1)
        f1 = np.round(info1[0],1)
        a1 = np.round(info1[1],1)
        return str.format('f0: {0}kHz  Amplitude0: {1}dB f1: {2}kHz Amplitude1: {3}dB df: {4}kHz dAmplitude: {5}dB',f0,a0 ,f1, a1,np.abs(f1-f0),np.abs(a1-a0))

    def getStrPoint(self, info):
        return str.format('Frequency: {0}kHz  Amplitude: {1}dB',np.round(info[0],1),np.round(info[1],1))

class Envelope(OneDimensionalFunction):
    def __init__(self,widget):
        OneDimensionalFunction.__init__(self,widget)
        self.myOptions = {u'name': u'Envelope', u'type': u'group', u'children':[
            {u'name':u'Amplitude', u'type':u'group', u'children':[
                {u'name':u'Min', u'type':u'float', u'value': -100, u'step': 0.1, 'default': -100},
                {u'name':u'Max', u'type':u'float', u'value': 100, u'step': 0.1, 'default': 100}
            ]},
            {u'name':u'Apply Function', u'type':'action'},
         ]}

    def connectMySignal(self,pTree):
        OneDimensionalFunction.connectMySignal(self,pTree)
        self.pTree.param('Envelope', 'Apply Function').sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalFunction.processing(self)
        max = self.pTree.param('Envelope').param('Amplitude').param('Max').value() * 0.01 * np.amax(self.widget.data)

        envelope = self.abs_decay_averaged_envelope(self.widget.data)
        # envelopeFactor = (2.0 ** (self.widget.bitdepth) * max / 100) / envelope[np.argmax(envelope)]
        # data = (envelopeFactor * envelope - 2 ** (self.widget.bitdepth - 1) * max / 100)

        self.widget.plot(envelope)

    def abs_decay_averaged_envelope(self,data, decay=1,softfactor=6,progress= None,position= (5,15),type="sin"):
        """
        decay is the min number of samples in data that separates two elements
        """
        progress_interval = position[1]-position[0]
        if progress is not None:
            progress(position[0]+progress_interval/10.0)
        rectified = np.array(abs(data))
        if progress is not None:
            progress(position[0]+progress_interval/5.0)
        i = 1
        arr = np.zeros(len(rectified), dtype=np.int32)
        current = rectified[0]
        fall_init = None
        progress_size = len(arr)/8.0

        while i < len(arr):
            if fall_init is not None:
                value = rectified[fall_init]
                if type=="lineal":
                    value -= rectified[fall_init]*(i-fall_init)/decay #lineal
                elif type=="sin":
                    value = rectified[fall_init]*np.sin(((i-fall_init)*1.0*np.pi)/(decay*2)+np.pi/2)
                elif type=="cuadratic":
                    value = rectified[fall_init]*(1-((i-fall_init)*1.0)/decay)**2

                arr[i-1] = max(value, rectified[i])
                fall_init = None if(value <= rectified[i] or i-fall_init >= decay) else fall_init
            else:
                fall_init = i-1 if rectified[i] < current else None
                arr[i-1] = current
            current = rectified[i]
            i += 1
            if i % progress_size == 0 and progress is not None:
                progress(position[0]+(i/progress_size)*progress_interval/10.0)
        arr[-1] = current

        if softfactor > 1:
            return np.array([np.mean(arr[i-softfactor:i]) for i,_ in enumerate(arr, start=softfactor)])
        return arr

class InstantaneousFrequencies(OneDimensionalFunction):
    def __init__(self,widget):
        OneDimensionalFunction.__init__(self,widget)
        self.myOptions = {u'name': u'Instantaneous Frequency', u'type': u'group', u'children':[{u'name':'Apply Function', u'type':'action'}]}

    def connectMySignal(self,pTree):
        OneDimensionalFunction.connectMySignal(self,pTree)
        self.pTree.param('Instantaneous Frequency', 'Apply Function').sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalFunction.processing(self)

        minx = self.widget.rangeX[0]
        maxx = max(self.widget.rangeX[1], min(minx + self.widget.NFFTSpec, len(self.widget.data)))
        data = self.widget.data[minx:maxx]

        Pxx, freqs, bins = mlab.specgram(data, Fs=self.widget.Fs)
        dtemp =  freqs[np.argmax(Pxx[1:len(Pxx)], axis=0)]

        self.widget.updateInterval(minx,maxx)
        self.widget.lastProc = self.processing
        self.widget.Pxx = Pxx
        self.widget.freqs = freqs
        self.widget.bins = bins
        self.widget.plot(bins[dtemp>0],dtemp[dtemp>0], clear=True, pen=None, symbol = 's', symbolSize = 1,symbolPen = self.widget.plotColor)
        self.widget.setRange(xRange = (0,bins[len(bins) - 1]),yRange=(0, self.widget.Fs/2),padding=0,update=True)
        self.widget.getPlotItem().showGrid(x=self.widget.gridX, y=self.widget.gridY)
        self.widget.getPlotItem().setLabel(axis='bottom',text='<font size=6>Time(s)<\\font>')
        self.widget.getPlotItem().setLabel(axis='left', text='<font size=6>Frequency<\\font>', units='<font size=6>Hz<\\font>')
        self.widget.getPlotItem().setTitle(title='<font size=6>Instantaneous Frequency<\\font>')
        self.widget.updateViewBox()
        self.widget.show()

    def getInfo(self, x):
        index = np.searchsorted(self.widget.bins,x)
        maxfreqs = np.argmax(self.widget.Pxx[1:len(self.widget.Pxx)], axis=0)
        freq = self.widget.freqs[maxfreqs][index]
        amp = 10*np.log10(self.widget.Pxx[np.searchsorted(self.widget.freqs,freq)][index]/np.amax(self.widget.Pxx))
        return [self.widget.bins[index], freq, amp]

    def getStr(self, info0, info1):
        t0 = info0[0]
        f0 = np.round(info0[1]/1000,1)
        a0 = np.round(info0[2],1)
        t1 = info1[0]
        f1 = np.round(info1[1]/1000,1)
        a1 = np.round(info1[2],1)
        return str.format('t0: {0}s f0: {1}kHz  Amplitude0: {2}dB t1: {3}s  f0: {4}kHz  Amplitude1: {5}dB dt: {6}s df: {7}kHz dAmplitude: {8}dB',t0,f0,a0,t1,f1,a1,np.abs(t1-t0),np.abs(f1-f0), np.abs(a1-a0))

    def getStrPoint(self, info):
        return str.format('Time: {0}s  Frequency: {1}kHz Amplitude: {2}dB  ' ,info[0],np.round(info[1]/1000,1),np.round(info[2],1))

class AveragePowSpec(OneDimensionalFunction):
        def __init__(self,widget):
            OneDimensionalFunction.__init__(self,widget)
            self.myOptions = {u'name': u'Power spectrum(Average)', u'type': u'group', u'children': [
            {u'name':u'FFT size', u'type': u'list', u'default':512, u'values': [(u'Automatic', 512),(u"128", 128), (u"256", 256),(u"512", 512), (u"1024", 1024)], u'value': u'512'},
            {u'name': u'FFT window', u'type': u'list', u'value':self.windows.Hamming,u'default':self.windows.Hamming,
             u'values': [(u"Hamming", self.windows.Hamming),(u'Bartlett',self.windows.Bartlett),(u"Blackman", self.windows.Blackman), (u"Hanning", self.windows.Hanning),(u'Kaiser',self.windows.Kaiser),(u'None',self.windows.WindowNone),(u"Rectangular", self.windows.Rectangular)]},
            {u'name': u'FFT overlap', u'type': u'int', u'value':50, u'limits': (-1, 99)},
            {u'name': u'Apply Function', u'type': u'action'},
        ]}

        def connectMySignal(self,pTree):
            self.pTree = pTree
            self.pTree.param('Power spectrum(Average)', 'Apply Function').sigActivated.connect(self.processing)

        def processing(self):
            OneDimensionalFunction.processing(self)
            window = self.pTree.param('Power spectrum(Average)', 'FFT window').value()
            NFFT = self.pTree.param('Power spectrum(Average)', 'FFT size').value()
            overlap = self.pTree.param('Power spectrum(Average)', 'FFT overlap').value() * NFFT/100.

            minx = self.widget.rangeX[0]
            maxx = max(self.widget.rangeX[1], min(minx + NFFT, len(self.widget.data)))
            data = self.widget.data[minx:maxx]

            (Pxx , freqs) = mlab.psd(data, Fs= self.widget.Fs, NFFT=NFFT, window=window, noverlap=overlap, scale_by_freq=False)
            Pxx.shape = len(freqs)

            self.widget.updateInterval(minx,maxx)
            self.widget.Pxx = Pxx
            self.widget.freqs = freqs
            db = 10*np.log10(Pxx/np.amax(Pxx))
            self.widget.plot(freqs/1000, db,clear=True, pen = self.widget.plotColor, symbol = 's', symbolSize = 1,symbolPen = self.widget.plotColor)
            self.widget.setRange(xRange = (0,freqs[len(freqs) - 1]/1000),yRange = (np.amin(db),0) ,padding=0,update=True)
            self.widget.setBackground(self.widget.backColor)
            self.widget.getPlotItem().showGrid(x=self.widget.gridX, y=self.widget.gridY)
            self.widget.getPlotItem().setLabel(axis='bottom',text='<font size=6>Frequency (kHz)<\\font>')
            self.widget.getPlotItem().setLabel(axis='left', text='<font size=6>Intensity<\\font>', units='<font size=6>dB<\\font>')
            self.widget.getPlotItem().setTitle(title='<font size=6>Power spectrum(Average)<\\font>')
            self.widget.updateViewBox()
            self.widget.show()

        def getInfo(self,x):
            index = np.searchsorted(self.widget.freqs,x*1000)
            freq = self.widget.freqs[index]
            amplt = 10*np.log10(self.widget.Pxx[index]/np.amax(self.widget.Pxx))
            return [freq/1000, amplt]


        def getStr(self, info0, info1):
            f0 = np.round(info0[0],1)
            a0 = np.round(info0[1],1)
            f1 = np.round(info1[0],1)
            a1 = np.round(info1[1],1)
            return str.format('f0: {0}kHz  Amplitude0: {1}dB f1: {2}kHz Amplitude1: {3}dB df: {4}kHz dAmplitude: {5}dB',f0,a0 ,f1, a1,np.abs(f1-f0),np.abs(a1-a0))

        def getStrPoint(self, info):
            return str.format('Frecuencia: {0}kHz  Amplitud: {1}dB', np.round(info[0], 1), np.round(info[1], 1))

class PowSpecPlotWidget(pg.PlotWidget):

    def __init__(self, parent=None,**kargs):
        self.gridX = True
        self.gridY = True
        self.lines = False
        self.wSettings = []

        self.proc = [LogarithmicPowSpec(self), AveragePowSpec(self), InstantaneousFrequencies(self)]
        self.lastProc = lambda : None
        self.getInfo = lambda  : None
        self.getStr = lambda : None
        self.getStrPoint = lambda : None

        self.windows = FFTWindows()
        pg.PlotWidget.__init__(self, **kargs)
        self.mousePressed = False
        pg.LegendItem()
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        self.getPlotItem().showGrid(x=self.gridX, y=self.gridY)
        #self.xLine = pg.InfiniteLine(angle = 90,pen=(0,9))
        #self.yLine = pg.InfiniteLine(angle = 0,pen=(0,9))
        #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.selectedTool = Tools.PointerCursor

        self.getPlotItem().getViewBox().addItem(self.pointerCursor)
        #self.getPlotItem().getViewBox().addItem(self.xLine)
        #self.getPlotItem().getViewBox().addItem(self.yLine)
        self.getPlotItem().setMouseEnabled(False,False)
        self.mouseReleased = False
        self.last = []
        self.freqs =[]
        self.Pxx =[]
        self.bins = []

    PointerChanged = pyqtSignal(str)
    PointerCursorPressed = pyqtSignal()
    PIXELS_OF_CURSORS_CHANGES = 5

    def updateViewBox(self):
        gem = self.parent().geometry()
        self.parent().resize(gem.width() / 3, gem.height())
        self.parent().resize(gem.width(), gem.height())

    def refresh(self):
        self.lastProc()

    def updateLast(self,range):
        self.rangeX = range
        self.lastProc()

    def setData(self,data,range, bitdepth,rate, NFFTSpec, updateInterval):
        self.data = data
        self.rangeX = range
        self.NFFTSpec = NFFTSpec
        self.bitdepth = bitdepth
        self.Fs = rate
        self.updateInterval = updateInterval

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
            info = self.getInfo(x)

            #self.xLine.setValue(info[0])
            #self.yLine.setValue(info[1])

            if self.mouseReleased:
                 # info0 = self.getInfo(self.last['pos'][0])
                 self.PointerChanged.emit(self.getStr(self.last, info))
            else:
                self.PointerChanged.emit(self.getStrPoint(info))
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
            info = self.getInfo(x)
            if not insidex:
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))
                return
            self.last = info
            last = {'pos':[info[0],info[1]], 'pen': {'color': 'w', 'width': 2},'brush':pg.intColor(255, 255), 'symbol':'+', 'size':20}
            self.pointerCursor.addPoints([last])
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
        return (a + (xPixel - minx) * np.abs(( b - a ) * 1. / (maxx - minx)),inside)

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        inside = True
        vb = self.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.getPlotItem().viewRange()[1]
        # yPixel = maxy - yPixel
        if yPixel < miny:
            inside = False
            yPixel = miny
        if yPixel > maxy:
            inside = False
            yPixel = maxy
        return (a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0)), inside)

    def loadTheme(self,Fs, window, plotColor,backColor, lines, maxY, minY, gridX, gridY):
        self.Fs = Fs
        self.window = window
        self.plotColor = plotColor
        self.lines = lines
        self.maxY = maxY
        self.minY = minY
        self.backColor = backColor

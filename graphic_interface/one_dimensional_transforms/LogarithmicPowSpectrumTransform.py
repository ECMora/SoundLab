# -*- coding: utf-8 -*-
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from graphic_interface.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np


class LogarithmicPowSpec(OneDimensionalTransform):
    def __init__(self, signal=None):
        OneDimensionalTransform.__init__(self, signal=signal)

    def _getParameterTree(self):
        params = [{u'name': unicode(self.tr(u'Power spectrum(Logarithmic)')), u'type':
        u'group', u'children': [
        {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
         u'value': WindowFunction.Rectangular, u'default': WindowFunction.Rectangular,
             u'values': [(u'Bartlett', WindowFunction.Bartlett),
                         (u"Blackman", WindowFunction.Blackman),
                         (u"Hamming", WindowFunction.Hamming),
                         (u"Hanning", WindowFunction.Hanning),
                         (u'Kaiser', WindowFunction.Kaiser),
                         (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                         (u"Rectangular", WindowFunction.Rectangular)]}
        ]}]

        parameter = self._createParameter(params)

        return self._createParameterTree(parameter)

    def connectMySignal(self,pTree):
        OneDimensionalTransform.connectMySignal(self,pTree)
        self.pTree.param(unicode(self.tr(u'Power spectrum(Logarithmic)')), unicode(self.tr(u'Apply Function'))).sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalTransform.processing(self)

        minx = self.widget.rangeX[0]
        maxx = max(self.widget.rangeX[1], min(minx + self.widget.NFFTSpec, len(self.widget.data)))
        data = self.widget.data[minx:maxx]

        window = self.pTree.param(unicode(self.tr(u'Power spectrum(Logarithmic)')), unicode(self.tr(u'FFT window'))).value()
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
        return str.format('f0: {0}kHz  ' + self.tr('Amplitude') + '0: {1}dB f1: {2}kHz ' + self.tr('Amplitude') \
                          + '1: {3}dB df: {4}kHz ' + self.tr('dAmplitude') + \
                          ': {5}dB', f0, a0, f1, a1, np.abs(f1-f0), np.abs(a1-a0))

    def getStrPoint(self, info):
        return str.format(self.tr('Frequency') + ': {0}kHz  ' + self.tr('Amplitude')
                          + ': {1}dB', np.round(info[0], 1), np.round(info[1], 1))



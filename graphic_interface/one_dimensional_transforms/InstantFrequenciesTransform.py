# -*- coding: utf-8 -*-
from graphic_interface.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
from matplotlib import mlab
import numpy as np


class InstantFrequencies(OneDimensionalTransform):
    def __init__(self, signal=None):
        OneDimensionalTransform.__init__(self, signal=None)

    def _getParameterTree(self):
        params = [{u'name': unicode(self.tr(u'Instantaneous Frequency')), u'type':
            u'group', u'children':[]}]

        parameter = self._createParameter(params)

        return self._createParameterTree(parameter)

    def processing(self):
        OneDimensionalTransform.processing(self)

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
        return str.format('t0: {0}s f0: {1}kHz  '+
                          self.tr('Amplitude') + '0: {2}dB t1: {3}s  f0: {4}kHz  ' +
                          self.tr('Amplitude') + '1: {5}dB dt: {6}s df: {7}kHz '+
                          self.tr('dAmplitude') + ': {8}dB', t0, f0, a0, t1, f1, a1,
                          np.abs(t1-t0),np.abs(f1-f0), np.abs(a1-a0))

    def getStrPoint(self, info):
        return str.format(self.tr('Time') +\
                          ': {0}s  ' + self.tr('Frequency') + ': {1}kHz '+\
                          self.tr('Amplitude') +\
                          ': {2}dB  ', info[0], np.round(info[1]/1000, 1), np.round(info[2], 1))
from PyQt4.QtCore import QObject, pyqtSignal
from matplotlib import mlab
import numpy as np
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from Utils.Utils import FLOATING_POINT_EPSILON
from duetto.audio_signals import AudioSignal
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction


class OneDimensionalFunction(QObject):
    """

    """

    # SIGNALS
    # signal raised when the parameters of the transform change
    # and the transform data must be recomputed
    dataChanged = pyqtSignal()

    def __init__(self, signal=None):
        QObject.__init__(self)
        # the parameter object with the set of parameters for the tree widget
        self.parameter = None

        # the parameter tree widget with the options
        self._parameterTree = self._getParameterTree()



        self._signal = signal

    def _getParameterTree(self):
        """
        Abstract method to implement in descendants.
        :return: returns the parameter tree with the visual options
        for the user interaction of the one dimensional function
        """
        return self._createParameterTree(self._createParameter([]))

    def _createParameter(self, params):
        """
        create and returns a parameter tree with the params supplied
        :param params:
        :return:
        """
        ListParameter.itemClass = DuettoListParameterItem
        ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        return ParamTree

    def _createParameterTree(self,parameter):
        """
        Create the parameter tree widget with the parameter supplied
        :param parameter: The pyqtgraph Parameter to insert in the tree widget
        :return:
        """
        parameterTree = ParameterTree()
        parameterTree.setAutoScroll(True)
        parameterTree.setHeaderHidden(True)
        parameterTree.setParameters(parameter, showTop=False)

        return parameterTree

    # region Properties signal, settings
    @property
    def settings(self):
        """
        Parameter tree widget with the visual settings
        of the function. Used for add it in a widget layout
        and interact with the user.
        :return:
        """
        return self._parameterTree

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        Modify and update the internal variables that uses the signal.
        :param new_signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if new_signal is None or not isinstance(new_signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")
        self._signal = new_signal

    # endregion

    def getData(self, indexFrom, indexTo):
        """
        Computes and returns the one dimensional transform
        over the signal data in the supplied interval.
        :param indexFrom: the start of the signal interval to process in signal array data indexes.
        :param indexTo: the end of the signal interval to process in signal array data indexes..
        """
        return np.zeros(indexTo-indexFrom)


class Envelope(OneDimensionalFunction):
    def __init__(self, signal=None):
        # the processing options for the envelope transform
        self.decay = 1.00
        self.softfactor = 6
        self.function_type = "sin"

        OneDimensionalFunction.__init__(self, signal=signal)

    def _getParameterTree(self):
        # create the tree with the params of the envelope one dim transform
        params = [{u'name': unicode(self.tr(u'Envelope')), u'type': u'group',
                   u'children': [
                       {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5},
                       {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'int', u'value': 6, u'step': 1},
                       {u'name': unicode(self.tr(u'Function Type')), u'type': u'list', u'value': "sin",
                        u'default': "sin",
                        u'values': [(u"Sin", "sin"),
                                    (u'Lineal', "lineal"),
                                    (u"Cuadratic", "cuadratic")]}
                   ]}]

        self.parameter = self._createParameter(params)

        # connect to register the changes on the param tree
        self.parameter.sigTreeStateChanged.connect(self.parameterChanged)

        return self._createParameterTree(self.parameter)

    def parameterChanged(self, param, changes):
        """
        Method that listen to the changes on the parameter tree and change the
        internal variables.
        :param param: The parameter tree
        :param changes: the changes made
        :return:
        """
        if self.parameter is None:
            return

        data_changed = False

        for param, change, data in changes:
            path = self.parameter.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Decay (ms)'))and self.decay != data:

                self.decay = data
                data_changed = True

            elif childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Soft Factor')) and self.softfactor != data:

                self.softfactor = data
                data_changed = True

            elif childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Function Type')) and self.function_type != data:
                self.function_type = data
                data_changed = True

        if data_changed:
            self.dataChanged.emit()

    def getData(self, indexFrom, indexTo):
            envelope = self.abs_decay_averaged_envelope(self.signal.data[indexFrom:indexTo], self.decay, self.softfactor,
                                                        self.function_type)
            return envelope

    def abs_decay_averaged_envelope(self, data, decay=1, softfactor=6, type="sin"):
            """
            decay is the min number of samples in data that separates two elements
            """

            rectified = np.array(abs(data))

            i = 1
            arr = np.zeros(len(rectified), dtype=np.int32)
            current = rectified[0]
            fall_init = None

            while i < len(arr):
                if fall_init is not None:
                    value = rectified[fall_init]
                    if type == "lineal":
                        value -= rectified[fall_init] * (i - fall_init) / decay  # lineal
                    elif type == "sin":
                        value = rectified[fall_init] * np.sin(((i - fall_init) * 1.0 * np.pi) / (decay * 2) + np.pi / 2)
                    elif type == "cuadratic":
                        value = rectified[fall_init] * (1 - ((i - fall_init) * 1.0) / decay) ** 2

                    arr[i - 1] = max(value, rectified[i])
                    fall_init = None if (value <= rectified[i] or i - fall_init >= decay) else fall_init
                else:
                    fall_init = i - 1 if rectified[i] < current else None
                    arr[i - 1] = current
                current = rectified[i]
                i += 1

            arr[-1] = current

            if softfactor > 1:
                return np.array([np.mean(arr[i - softfactor:i]) for i, _ in enumerate(arr, start=softfactor)])
            return arr


class AveragePowSpec(OneDimensionalFunction):
    def __init__(self, signal=None):
        OneDimensionalFunction.__init__(self, signal=signal)

        self.window = WindowFunction.Rectangular
        self.NFFT = 512
        self.overlap = 256

    def _getParameterTree(self):
        params = [ {u'name': unicode(self.tr(u'Power spectrum(Average)')), u'type': u'group',
                u'children': [
                    {u'name':unicode(self.tr(u'FFT size')), u'type': u'list', u'default':512,
                     u'values': [(unicode(self.tr(u'Automatic')), 512),
                                 (u"128", 128), (u"256", 256),
                                 (u"512", 512), (u"1024", 1024)],
                     u'value': 512},
                    {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
                     u'value': WindowFunction.Rectangular, u'default': WindowFunction.Rectangular,
                     u'values': [(u'Bartlett', WindowFunction.Bartlett),
                                 (u"Blackman", WindowFunction.Blackman),
                                 (u"Hamming", WindowFunction.Hamming),
                                 (u"Hanning", WindowFunction.Hanning),
                                 (u'Kaiser', WindowFunction.Kaiser),
                                 (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                                 (u"Rectangular", WindowFunction.Rectangular)]},
                    {u'name': unicode(self.tr(u'FFT overlap')), u'type': u'int',
                     u'value': 50, u'limits': (1, 99)}]}]

        self.parameter = self._createParameter(params)

        # connect to register the changes on the param tree
        self.parameter.sigTreeStateChanged.connect(self.parameterChanged)

        return self._createParameterTree(self.parameter)

    def parameterChanged(self, param, changes):
        """
        Method that listen to the changes on the parameter tree and change the
        internal variables.
        :param param: The parameter tree
        :param changes: the changes made
        :return:
        """
        if self.parameter is None:
            return

        data_changed = False

        for param, change, data in changes:
            path = self.parameter.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Power spectrum(Average)')) + \
                    u'.' + unicode(self.tr(u'FFT window')) and self.window != data:

                self.window = data
                data_changed = True

            elif childName == unicode(self.tr(u'Power spectrum(Average)')) + \
                    u'.' + unicode(self.tr(u'FFT size')) and self.NFFT != data:

                self.NFFT = data
                data_changed = True

            elif childName == unicode(self.tr(u'Power spectrum(Average)')) + \
                    u'.' + unicode(self.tr(u'FFT overlap')) and abs(self.__getOverlap(data)-self.overlap) < FLOATING_POINT_EPSILON:
                self.overlap = self.__getOverlap(data)
                data_changed = True

        if data_changed:
            self.dataChanged.emit()

    def __getOverlap(self, overlap_percent):
        """
        get the number of points of overlap from the percent value supplied.
        :param overlap_percent: the percent of overlap form the NFFT value.
        :return:
        """
        return self.NFFT * overlap_percent/100.0

    def getData(self, indexFrom, indexTo):

        data = self.signal.data[indexFrom:indexTo]

        (Pxx, freqs) = mlab.psd(data, NFFT=self.NFFT, window=self.window,
                                       noverlap=self.overlap, scale_by_freq=False)
        Pxx.shape = len(freqs)

        return 10*np.log10(Pxx/np.amax(Pxx))


class LogarithmicPowSpec(OneDimensionalFunction):
    def __init__(self, signal=None):
        OneDimensionalFunction.__init__(self, signal=signal)

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
        OneDimensionalFunction.connectMySignal(self,pTree)
        self.pTree.param(unicode(self.tr(u'Power spectrum(Logarithmic)')), unicode(self.tr(u'Apply Function'))).sigActivated.connect(self.processing)

    def processing(self):
        OneDimensionalFunction.processing(self)

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


class InstantaneousFrequencies(OneDimensionalFunction):
    def __init__(self, signal=None):
        OneDimensionalFunction.__init__(self, signal=None)

    def _getParameterTree(self):
        params = [{u'name': unicode(self.tr(u'Instantaneous Frequency')), u'type':
            u'group', u'children':[]}]

        parameter = self._createParameter(params)

        return self._createParameterTree(parameter)

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
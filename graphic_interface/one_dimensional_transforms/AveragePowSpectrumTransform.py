# -*- coding: utf-8 -*-
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from graphic_interface.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np
import matplotlib as mlab


class AveragePowSpec(OneDimensionalTransform):
    def __init__(self, signal=None):
        OneDimensionalTransform.__init__(self, signal=signal)

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
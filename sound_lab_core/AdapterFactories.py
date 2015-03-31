# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from sound_lab_core.Clasification.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.Segmentation.Detectors.Adapters import *


class AdapterFactory(QObject):
    def __init__(self):
        QObject.__init__(self)
        # list of (name, adapter)
        self.adapters = []

    def adapters_names(self):
        """
        Gets the name of all registered adapters.
        :return: a list of str, each the name of one adapter
        """
        return [x[0] for x in self.adapters]

    def get_adapter(self, name):
        """
        Gets an get_instance of the corresponding one dimensional transform given its name.
        :param name: a str, the name of the transform. Must be one of the values returned by the get_all_transforms_names method.
        :return: an get_instance of the corresponding one dimensional transform
        """
        for i in range(len(self.adapters)):
            if name == self.adapters[i][0]:
                return self.adapters[i][1]

        raise Exception("Not found adapter")


class ParameterGroup:
    def __init__(self, name, adapters):
        self.name = name
        self.adapters = adapters

    def adapters_names(self):
        return [x[0] for x in self.adapters]

    def get_adapter(self, name):
        for i in range(len(self.adapters)):
            if name == self.adapters[i][0]:
                return self.adapters[i][1]

        raise Exception("Not found adapter")


class ParametersAdapterFactory(QObject):
    def __init__(self):
        QObject.__init__(self)

        time_params_adapters = [
            (u'Start Time', StartTimeParameterAdapter()),
            (u'End Time', EndTimeParameterAdapter()),
            (u'Duration', DurationTimeParameterAdapter()),
            (u'Zero Cross Rate', ZeroCrossRateParameterAdapter()),
            (u'Local Max Mean', LocalMaxMeanParameterAdapter()),
            (u'Entropy', EntropyTimeParameterAdapter())]

        wave_params_adapters = [
            (u'RMS', RmsTimeParameterAdapter()),
            (u'PeakToPeak', PeakToPeakParameterAdapter()),
            (u'StartToMax', StartToMaxTimeParameterAdapter())]

        spectral_params_adapters = [
            (u'PeakFreq', PeakFreqParameterAdapter()),
            (u'MaxFreq', MaxFreqParameterAdapter()),
            (u'MinFreq', MinFreqParameterAdapter()),
            (u'BandWidth', BandWidthParameterAdapter()),
            (u'PeaksAbove', PeaksAboveParameterAdapter())]

        self.parameter_groups = [ParameterGroup(unicode(self.tr(u"Time Parameters")), time_params_adapters),
                                 ParameterGroup(unicode(self.tr(u"Wave Parameters")), wave_params_adapters),
                                 ParameterGroup(unicode(self.tr(u"Spectral Parameters")), spectral_params_adapters),
                                 ]

    def get_adapter(self, name):
        for group in self.parameter_groups:
            try:
                adapter = group.get_adapter(name)
                if adapter:
                    return adapter
            except Exception as ex:
                pass

        raise Exception("Not found adapter")


class SegmentationAdapterFactory(AdapterFactory):
    def __init__(self):
        AdapterFactory.__init__(self)

        self.adapters = [
            (u'Manual', ManualDetectorAdapter()),
            (u'Envelope Abs Decay', AbsDecayEnvelopeDetectorAdapter()),
            (u'Interval Rms', IntervalRmsDetectorAdapter()),
            (u'Interval Max Mean', IntervalMaxMeanDetectorAdapter()),
            (u'Interval Power Spectrum', IntervalPowerSpectrumDetectorAdapter()),
            (u'Watershed', WatershedDetectorAdapter()),
            (u'Adaptive Threshold', AdaptThreshDetectorAdapter()),
            (u'GrabCut', GrabCutDetectorAdapter())
        ]


class ClassificationAdapterFactory(AdapterFactory):
    def __init__(self):
        AdapterFactory.__init__(self)

        self.adapters = [(u'Manual',  ManualClassifierAdapter()),
                         (u'KNN', KNNClassifierAdapter()),
                         (u'Neural Nets', NeuralNetsAdapter())]

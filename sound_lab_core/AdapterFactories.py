# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from sound_lab_core.Clasification.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.Segmentation.Adapters import *


class AdapterFactory(QObject):
    """
    Class that provides the adapters for segmentation, classification
    and parameter measurement.
    """
    def __init__(self):
        QObject.__init__(self)

        # list of tuples (name, adapter). It's used a list instead of dict
        # to keep the order in the adapters and do not use a sorted dict
        # because is an short list
        self.adapters = []

    def adapters_names(self):
        """
        Gets the list of names of all registered adapters.
        :return: a list of str each one is the name of one adapter
        """
        return [x[0] for x in self.adapters]

    def get_adapter(self, name):
        """
        :return: an instance of the corresponding adapter transform
        :raise: Exception if no adapter is found with name supplied
        """
        # self.adapters contains tuples with shape (name, adapter)
        adapters = [x[1] for x in self.adapters if name == x[0]]

        if len(adapters) == 0:
            raise Exception("Not found adapter")

        return adapters[0]


class ParameterGroup:
    """
    Class that groups the parameters adapters into groups of
    similar behavior like the frequency measurers.
    """
    def __init__(self, name, adapters):
        # group name
        self.name = name

        # list of adapters in the group.
        # Is a list of tuples with shape (adapter_name, adapter_instance)
        self.adapters = adapters

    def adapters_names(self):
        """
        :return: All the name of adapters on the group
        """
        return [x[0] for x in self.adapters]

    def get_adapter(self, name):
        """
        :return: an instance of the corresponding adapter transform
        :raise: Exception if no adapter is found with name supplied
        """
        # self.adapters contains tuples with shape (name, adapter)
        adapters = [x[1] for x in self.adapters if name == x[0]]

        if len(adapters) == 0:
            raise Exception("Not found adapter")

        return adapters[0]


class ParametersAdapterFactory(QObject):
    """
    Factory for parameter measurement adapters.
    The parameters are grouped by category.
    """
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
        """
        Try to get the adapter in one of the groups.
        :param name: The name of the searched adapter
        :return: Adapter if found on one group. Raise exception if not adapter found
        with that name.
        """
        for group in self.parameter_groups:
            try:
                return group.get_adapter(name)

            except Exception as ex:
                pass

        raise Exception("Not found adapter")


class SegmentationAdapterFactory(AdapterFactory):
    def __init__(self):
        AdapterFactory.__init__(self)

        self.adapters = [
            (u'Manual', ManualDetectorAdapter()),
            (u'Interval Power Spectrum', IntervalPowerSpectrumDetectorAdapter()),
            (u'Interval Rms', IntervalRmsDetectorAdapter()),
            (u'Interval Max Mean', IntervalMaxMeanDetectorAdapter()),
            (u'Envelope Abs Decay', AbsDecayEnvelopeDetectorAdapter()),
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

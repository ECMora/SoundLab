from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.Segmentation.Detectors.Adapters import *
from sound_lab_core.Segmentation.Detectors.Adapters.IntervalMaxMeanDetectorAdapter import IntervalMaxMeanDetectorAdapter
from sound_lab_core.Segmentation.Detectors.Adapters.IntervalRmsDetectorAdapter import IntervalRmsDetectorAdapter


class AdapterFactory(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
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
    def __init__(self, parent=None):
        QObject.__init__(self)

        time_params_adapters = [
            (u'Start Time', StartTimeParameterAdapter(parent)),
            (u'End Time', EndTimeParameterAdapter(parent)),
            (u'Duration', DurationTimeParameterAdapter(parent))]
        wave_params_adapters = [
            (u'RMS', RmsTimeParameterAdapter(parent)),
            (u'PeakToPeak', PeakToPeakParameterAdapter(parent)),
            (u'StartToMax', StartToMaxTimeParameterAdapter(parent))]
        spectral_params_adapters = [
            (u'PeakFreq', PeakFreqParameterAdapter(parent)),
            (u'MaxFreq', MaxFreqParameterAdapter(parent)),
            (u'MinFreq', MinFreqParameterAdapter(parent)),
            (u'BandWidth', BandWidthParameterAdapter(parent)),
            (u'PeaksAbove', PeaksAboveParameterAdapter(parent))]

        self.parameter_groups = [ParameterGroup(unicode(self.tr(u"Time Parameters")),time_params_adapters),
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
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = [
            (u'Manual', ManualDetectorAdapter(parent)),
            (u'Envelope Abs Decay', AbsDecayEnvelopeDetectorAdapter(parent)),
            (u'Interval Rms', IntervalRmsDetectorAdapter(parent)),
            (u'Interval Max Mean', IntervalMaxMeanDetectorAdapter(parent)),
            (u'Watershed', WatershedDetectorAdapter(parent)),
            (u'Adaptive Threshold', AdaptThreshDetectorAdapter(parent)),
            (u'GrabCut', GrabCutDetectorAdapter(parent))
        ]


class ClassificationAdapterFactory(AdapterFactory):
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = [
            (u'Manual', None)
        ]

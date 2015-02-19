from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.Segmentation.Detectors.Adapters import *


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


class ParametersAdapterFactory(AdapterFactory):
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = [
            (u'Start Time', StartTimeParameterAdapter(parent)),
            (u'End Time', EndTimeParameterAdapter(parent)),
            (u'Duration', DurationTimeParameterAdapter(parent)),
            (u'RMS', RmsTimeParameterAdapter(parent)),
            (u'PeakToPeak', PeakToPeakParameterAdapter(parent)),
            (u'StartToMax', StartToMaxTimeParameterAdapter(parent)),
            (u'PeakFreq', PeakFreqParameterAdapter(parent)),
            (u'MaxFreq', MaxFreqParameterAdapter(parent)),
            (u'MinFreq', MinFreqParameterAdapter(parent)),
            (u'BandWidth', BandWidthParameterAdapter(parent)),
            (u'PeaksAbove', PeaksAboveParameterAdapter(parent))
        ]


class SegmentationAdapterFactory(AdapterFactory):
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = [
            (u'Envelope Abs Decay', AbsDecayEnvelopeDetectorAdapter(parent)),
            (u'Manual', ManualDetectorAdapter(parent)),
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

from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.Segmentation.Detectors.Adapters import *


class AdapterFactory(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.adapters = {}

    def adapters_names(self):
        """
        Gets the name of all registered adapters.
        :return: a list of str, each the name of one adapter
        """
        return self.adapters.keys()

    def get_adapter(self, name):
        """
        Gets an get_instance of the corresponding one dimensional transform given its name.
        :param name: a str, the name of the transform. Must be one of the values returned by the get_all_transforms_names method.
        :return: an get_instance of the corresponding one dimensional transform
        """
        if name not in self.adapters:
            raise Exception("Not found adapter")

        return self.adapters[name]


class ParametersAdapterFactory(AdapterFactory):

    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = {
            'Start Time': StartTimeParameterAdapter(parent),
            'End Time': EndTimeParameterAdapter(parent),
            'Duration': DurationTimeParameterAdapter(parent),
            'RMS': RmsTimeParameterAdapter(parent),
            'PeekToPeek': PeekToPeekParameterAdapter(parent)
        }


class SegmentationAdapterFactory(AdapterFactory):
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = {
            'Manual': ManualDetectorAdapter(parent),
            'Envelope Abs Decay': AbsDecayEnvelopeDetectorAdapter(parent)
        }


class ClassificationAdapterFactory(AdapterFactory):
    def __init__(self, parent=None):
        AdapterFactory.__init__(self, parent)

        self.adapters = {
            'Manual': None
        }
